from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from apps.accounts.models import User
from apps.api.serializers.auth import (
    LoginSerializer,
    LoginResponseSerializer,
    UserSerializer,
    MembershipSerializer
)

from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

@extend_schema(
    summary="Login",
    description="Autentica usuário e retorna tokens JWT (access e refresh).",
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            response=LoginResponseSerializer,
            description="Login realizado com sucesso"
        ),
        401: OpenApiResponse(description="Credenciais inválidas")
    },
    tags=['auth']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Endpoint de login com JWT.
    """
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    
    # Busca usuário por email
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {'detail': 'Credenciais inválidas.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # ⭐ CORREÇÃO: Autentica com USERNAME ao invés de email
    # Como seu User usa email como USERNAME_FIELD, passa o email diretamente
    user_authenticated = authenticate(request, username=email, password=password)
    
    if user_authenticated is None:
        return Response(
            {'detail': 'Credenciais inválidas.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    if not user_authenticated.is_active:
        return Response(
            {'detail': 'Usuário inativo.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Gera tokens JWT
    refresh = RefreshToken.for_user(user_authenticated)
    
    # Busca memberships do usuário
    memberships = user_authenticated.memberships.filter(is_active=True).select_related(
        'organization', 'office'
    )
    
    # Monta resposta
    response_data = {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': UserSerializer(user_authenticated).data,
        'memberships': MembershipSerializer(memberships, many=True).data
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@extend_schema(
    summary="Logout",
    description="Invalida o refresh token (adiciona à blacklist).",
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'refresh': {'type': 'string', 'description': 'Refresh token'}
            },
            'required': ['refresh']
        }
    },
    responses={
        200: OpenApiResponse(description="Logout realizado com sucesso"),
        400: OpenApiResponse(description="Token inválido")
    },
    tags=['auth']
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Endpoint de logout (blacklist do refresh token).
    """
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response(
            {'detail': 'Logout realizado com sucesso.'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'detail': 'Token inválido.'},
            status=status.HTTP_400_BAD_REQUEST
        )

@extend_schema(
    summary="Dados do usuário",
    description="Retorna dados do usuário autenticado e seus memberships.",
    responses={
        200: OpenApiResponse(
            response={
                'user': UserSerializer,
                'memberships': MembershipSerializer(many=True)
            }
        )
    },
    tags=['auth']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    """
    Retorna dados do usuário autenticado.
    """
    memberships = request.user.memberships.filter(is_active=True).select_related(
        'organization', 'office'
    )
    
    return Response({
        'user': UserSerializer(request.user).data,
        'memberships': MembershipSerializer(memberships, many=True).data
    })

@extend_schema(
    summary="Refresh token",
    description="Gera novo access token usando o refresh token.",
    tags=['auth']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token_view(request):
    """
    Refresh do access token usando refresh token.
    """
    from rest_framework_simplejwt.views import TokenRefreshView
    return TokenRefreshView.as_view()(request._request)
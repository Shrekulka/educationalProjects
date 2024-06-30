# backend/modules/system/urls.py

from django.urls import path, include

from .views import (
    ProfileUpdateView, ProfileDetailView, UserRegisterView, UserLoginView,
    UserPasswordChangeView, UserForgotPasswordView, UserPasswordResetConfirmView, EmailConfirmationSentView,
    UserConfirmEmailView, EmailConfirmedView, EmailConfirmationFailedView, UserLogoutView, FeedbackCreateView,
    ProfileFollowingCreateView
)

urlpatterns = [

    # URL для редактирования профиля текущего пользователя.
    # При обращении по этому URL вызывается класс-представление ProfileUpdateView.
    # Имя маршрута 'profile_edit'.
    path('user/edit/', ProfileUpdateView.as_view(), name='profile_edit'),

    # URL для просмотра профиля пользователя по его уникальному идентификатору (slug).
    # В URL указывается параметр <str:slug>, который будет передан в представление как аргумент.
    # При обращении по этому URL вызывается класс-представление ProfileDetailView.
    # Имя маршрута 'profile_detail'.
    path('user/<str:slug>/', ProfileDetailView.as_view(), name='profile_detail'),

    # URL для создания и удаления подписки на профиль пользователя.
    # В URL указывается параметр <str:slug>, который будет передан в представление как аргумент.
    # При обращении по этому URL вызывается класс-представление ProfileFollowingCreateView.
    # Имя маршрута 'follow'.
    path('user/follow/<str:slug>/', ProfileFollowingCreateView.as_view(), name='follow'),

    # URL для авторизации пользователя.
    # При обращении по этому URL вызывается класс-представление UserLoginView.
    # Имя маршрута 'login'.
    path('login/', UserLoginView.as_view(), name='login'),

    # URL для выхода пользователя из системы.
    # При обращении по этому URL вызывается класс-представление UserLogoutView.
    # Имя маршрута 'logout'.
    path('logout/', UserLogoutView.as_view(), name='logout'),

    # URL для изменения пароля пользователя.
    # При обращении по этому URL вызывается класс-представление UserPasswordChangeView.
    # Имя маршрута 'password_change'.
    path('password-change/', UserPasswordChangeView.as_view(), name='password_change'),

    # URL для запроса на восстановление пароля.
    # При обращении по этому URL вызывается класс-представление UserForgotPasswordView.
    # Имя маршрута 'password_reset'.
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),

    # URL для установки нового пароля после сброса.
    # В URL указываются параметры <uidb64> и <token>, которые будут переданы в представление как аргументы.
    # При обращении по этому URL вызывается класс-представление UserPasswordResetConfirmView.
    # Имя маршрута 'password_reset_confirm'.
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # URL для регистрации нового пользователя.
    # При обращении по этому URL вызывается класс-представление UserRegisterView.
    # Имя маршрута 'register'.
    path('register/', UserRegisterView.as_view(), name='register'),

    # URL для отображения сообщения об отправке письма с подтверждением email.
    # При обращении по этому URL вызывается класс-представление EmailConfirmationSentView.
    # Имя маршрута 'email_confirmation_sent'.
    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),

    # URL для подтверждения email пользователя.
    # В URL указываются параметры <uidb64> и <token>, которые будут переданы в представление как аргументы.
    # При обращении по этому URL вызывается класс-представление UserConfirmEmailView.
    # Имя маршрута 'confirm_email'.
    path('confirm-email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),

    # URL для отображения сообщения о подтверждении email.
    # При обращении по этому URL вызывается класс-представление EmailConfirmedView.
    # Имя маршрута 'email_confirmed'.
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),

    # URL для отображения сообщения о неудачном подтверждении email.
    # При обращении по этому URL вызывается класс-представление EmailConfirmationFailedView.
    # Имя маршрута 'email_confirmation_failed'.
    path('confirm-email-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),

    # URL для отображения формы обратной связи.
    # При обращении по этому URL вызывается класс-представление FeedbackCreateView.
    # Это представление позволяет пользователям отправлять обратную связь через контактную форму.
    # Имя маршрута 'feedback' используется для ссылки на этот URL в шаблонах и других частях кода.
    path('feedback/', FeedbackCreateView.as_view(), name='feedback'),

    # URL для обработки запросов на CAPTCHA.
    # При обращении по этому URL будут обработаны все запросы, связанные с капчей.
    path('captcha/', include('captcha.urls')),
]

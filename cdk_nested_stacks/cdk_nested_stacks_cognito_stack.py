from aws_cdk.aws_cognito import UserPool
from constructs import Construct
from aws_cdk import NestedStack, RemovalPolicy, Duration
from aws_cdk import aws_cognito as cognito


class CdkNestedStacksCognitoStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.user_pool = cognito.UserPool(
            self, 'nested-stack-cognito-user-pool',
            user_pool_name="nested-stack-cognito-user-pool",
            sign_in_aliases=cognito.SignInAliases(email=True),
            self_sign_up_enabled=True,
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            user_verification=cognito.UserVerificationConfig(
                # email_subject='You need to verify your email',
                # email_body='Thanks for signing up Your verification code is {####}',
                email_style=cognito.VerificationEmailStyle.LINK
            ),
            standard_attributes=cognito.StandardAttributes(
                family_name=cognito.StandardAttribute(
                    mutable=False,
                    required=True
                ),
                address=cognito.StandardAttribute(
                    mutable=True,
                    required=False
                )
            ),
            custom_attributes={
                'tenantId': cognito.StringAttribute(
                    mutable=False,
                    min_len=10,
                    max_len=15
                ),
                'createdAt': cognito.DateTimeAttribute(),
                'userId': cognito.NumberAttribute(
                    mutable=False,
                    min=1,
                    max=100
                ),
                'isAdmin': cognito.BooleanAttribute(
                    mutable=False
                )
            },
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=True
            ),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,

            removal_policy=RemovalPolicy.DESTROY
        )

        self.user_pool.add_client('nested-stack-cognito-app-client',
                             user_pool_client_name='nested-stack-cognito-app-client',
                             access_token_validity=Duration.minutes(60),
                             id_token_validity=Duration.minutes(60),
                             refresh_token_validity=Duration.days(1),
                             auth_flows=cognito.AuthFlow(user_password=True),
                             o_auth=cognito.OAuthSettings(
                                 flows=cognito.OAuthFlows(
                                     authorization_code_grant=True)),
                             # scopes=aws_cdk.aws_cognito.OAuthScope.resource_server(aws_cdk.aws_cognito.OAuthScope.OPENID, aws_cdk.aws_cognito.OAuthScope.resource_server(resource_server, nested-stack_api_read_scope))),
                             prevent_user_existence_errors=True,
                             generate_secret=False,
                             enable_token_revocation=True)

        self.user_pool.add_domain("nested-stack-cognito-domain",
                             cognito_domain=cognito.CognitoDomainOptions(
                                 domain_prefix="rachel-nested-stack-app"
                             )
                             )



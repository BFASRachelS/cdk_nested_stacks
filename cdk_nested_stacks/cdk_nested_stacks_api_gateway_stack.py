from aws_cdk.aws_apigateway import IntegrationResponse, MethodResponse, IntegrationResponse, MethodResponse
from constructs import Construct
from aws_cdk import App, CfnOutput, NestedStack, NestedStackProps, Stack, RemovalPolicy, Duration, Fn
from aws_cdk.aws_apigateway import Deployment, Method, MockIntegration, PassthroughBehavior, RestApi, Stage, \
    CognitoUserPoolsAuthorizer, StageOptions, EndpointType, CorsOptions, Cors, AuthorizationType
from cdk_nested_stacks.cdk_nested_stacks_cognito_stack import CdkNestedStacksCognitoStack

class CdkNestedStacksApiGatewayStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Using Nested stacks for Cognito
        user_pool = CdkNestedStacksCognitoStack(self, "CdkNestedStacksCognitoStack")

        rest_api = RestApi(
            self,
            "nested-stack-rest-api",
            deploy=True,
            deploy_options=StageOptions(stage_name='prod'),
            endpoint_types=[EndpointType.EDGE],
            default_cors_preflight_options=CorsOptions(
                allow_origins=Cors.ALL_ORIGINS,
                allow_methods=Cors.ALL_METHODS
            ),
            rest_api_name="nested-stack-rest-api",
            description="A test proxy integration"
        )

        cognito_user_pool_authorizer = CognitoUserPoolsAuthorizer(self, 'cognito-user_pool-authorizer',
                                                                  cognito_user_pools=[user_pool.user_pool]
                                                                  )

        # /nested-stack-api
        rest_api_resource = rest_api.root.add_resource('nested-stack-api')
        rest_api_resource.add_method(
            'GET',
            MockIntegration(
                integration_responses=[{
                    'statusCode': '200',
                    'responseTemplates': {
                        'application/json': '{"statusCode": 200, "message": "Hello From Protected Resource"}'
                    },
                    'responseParameters': {
                        'method.response.header.Content-Type': "'application/json'",
                        'method.response.header.Access-Control-Allow-Origin': "'*'"
                    }
                }],
                request_templates={
                    'application/json': "{ 'statusCode': 200 }"
                }
            ),
            method_responses=[{
                'statusCode': '200',
                'responseParameters': {
                    'method.response.header.Content-Type': True,
                    'method.response.header.Access-Control-Allow-Origin': True
                }
            }],
            authorizer=cognito_user_pool_authorizer,
            authorization_type=AuthorizationType.COGNITO,
            # authorization_scopes=['nested-stack-api-resource-server/nested-stack-api.read']
        )

# simple_qu_search

1. read ./init/README.md
2. openai api key as AWS SSM Secret Param
3. replace YOUR_SSM_OPENAI_API_KEY_NAME
4. make sam_build
5. make sam_deploy
6. add ssm param read permission to created iam role

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt",
                "secretsmanager:GetSecretValue",
                "ssm:GetParameters",
                "ssm:GetParameter"
            ],
            "Resource": [
                "arn:aws:secretsmanager:ap-northeast-1:YOUR_ACCOUNT_ID:secret:openai-api-key",
                "arn:aws:ssm:ap-northeast-1:YOUR_ACCOUNT_ID:parameter/openai-api-key"
            ]
        }
    ]
}
```

7. curl "https://YOUR_API_URL/Prod/qa?search_query=Database"
8. get response like below

```
[
  "ウェブサイトのデータベースとしてよく使われるものには、MySQL、PostgreSQL、MongoDB、SQLiteなどがあります。これらのデータベースは、データの保存、取得、操作などを効率的に行うために使用されます。選択するデータベースには、データの構造や関係、スケーラビリティなどを考慮する必要があります。", 
  "ウェブサイトのコンテンツ管理には、CMS（コンテンツ管理システム）が使われます。代表的なCMSとしてはWordPress、Drupal、Joomlaなどがあります。これらのツールを使用することで、コンテンツの作成、編集、公開などが容易に行えます。", 
  "ウェブサイトのセクションとしてよく使われるものには、ヘッダー、メニュー、ヒーローセクション、特徴やサービスの紹介セクション、お問い合わせフォーム、フッターなどがあります。これらのセクションは、ウェブサイトの構造やユーザーのナビゲーションをサポートする役割を果たします。"
]
```

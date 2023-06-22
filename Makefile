sam_init:
	sam init --runtime python3.10 --name simple-qa-lambda
sam_build:
	sam build --use-container
sam_deploy:
	sam deploy
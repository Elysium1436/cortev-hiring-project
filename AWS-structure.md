


## Containerizing
- Docker
- Amazon ECR

## App Deployment
Here, it depends. If we expect that we need to scale immensely, EKS or ECS is ideal. Else, App Runner or Elastic Beanstalk shoul dbe good to. 

## Database
Again, it depends on how big we're expecting this to be. If we need horizontal scalability, Amazon Aurora would be ideal, else, just using Amazon RDS would be fine. Also, since this is a geopraphical app, using geographical database extensions like PostGIS would be ideal.

## Schedule
Possible options are:
- Celery and celery schedule
- Amazon EventBridge Scheduler
- AWS lambda on cronjob

## CI/CD
- AWS CodePipeline

## Observability
- Amazon CloudWatch is fine. 
pipeline {
    agent any
    stages {
	
		stage('Stage: Compile Projects') {
			steps{
				sh 'mvn clean compile'
			}
		}
		
		stage('Stage: Unit Test') {
			steps {
				sh 'mvn test'
			}
		}
		
		stage('Stage: SonarQube Analysis') {
			steps {
				withSonarQubeEnv('sonarqube') {
					sh 'mvn sonar:sonar'
                }
			}
		}
		
		stage("Stage: Quality Gate") {
			steps {
				timeout(time:5, unit:'MINUTES'){
					sleep(10)
					waitForQualityGate abortPipeline:true
				}
			}
		}
		
		stage('Stage: Packaging') {
			steps {
				sh 'mvn package'
			}
		}
		
		stage('Stage: Deploy in WAS') {
			steps {
				lock(resource: 'deploy-to-websphere'){
					echo 'Deploying in WAS ..............'
					build job: 'deploy-to-websphere', parameters: [string(name: 'WAR_LOC', value: 'sample-application-cicd/target/*.war'), string(name: 'APP_NAME', value: 'SampleWebApplication')]
				}
			}
		}
    }
}

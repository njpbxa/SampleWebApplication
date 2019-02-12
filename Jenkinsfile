pipeline {
    agent any
    stages {
	
		stage('Compile Projects') {
			steps{
				sh 'mvn clean compile'
			}
		}
		
		stage('Unit Test') {
			steps {
				sh 'mvn test'
			}
		}
		
		stage('SonarQube Analysis') {
			steps {
				withSonarQubeEnv('sonarqube') {
					sh 'mvn clean package sonar:sonar'
                }
			}
		}
				
		stage("Quality Gate") {
			steps {
				timeout(time:5, unit:'MINUTES'){
					sleep(10)
					waitForQualityGate abortPipeline:true
				}
			}
		}
		
		stage('Packaging') {
			steps {
				sh 'mvn package'
			}
		}
		
		stage('Deploy in WAS') {
			steps {
				lock(resource: 'deploy-to-websphere'){
					echo 'Deploying in WAS ..............'
					build job: 'deploy-to-websphere', parameters: [string(name: 'WAR_LOC', value: 'sample-application-cicd/target/*.war'), string(name: 'APP_NAME', value: 'SampleWebApplication')]
				}
			}
		}
    }
}

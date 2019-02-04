pipeline {
    agent any
    stages {
		stage('Stage: Compile') {
			steps {
				echo 'Compiling the Projects ..............'
				withMaven(maven : 'maven_3_6_0'){
					sh 'mvn clean compile'
				}
			}
		}
		stage('Stage: Unit Test') {
			steps {
				echo 'Running Unit Tests ..............'
				withMaven(maven : 'maven_3_6_0'){
					sh 'mvn test'
				}
			}
		}
		
		stage('Stage: SonarQube Analysis') {
			steps {
				echo 'Generating Sonar report..'
				script {
					env.scannerHome = "${tool 'sonarqube'}"
					pom = readMavenPom file:'pom.xml'
					env.PROJECT_VERSION = pom.version
				}
				withSonarQubeEnv('sonarqube') {
					sh '
						echo "scannerHome = ${scannerHome}"
						echo "JAVA_HOME = ${JAVA_HOME}"
						echo "sonar.projectVersion = ${PROJECT_VERSION}"
					  '
					sh '${scannerHome}/bin/sonar-scanner -Dsonar.projectVersion="${PROJECT_VERSION}"'
				}
			}
		}

		stage("Stage: Quality Gate") {
			steps {
				timeout(time:1, unit:'HOURS'){
					waitForQualityGate abortPipeline:true
				}
			}
		}
		
		stage('Stage: Packaging') {
			steps {
				echo 'Packaging the Projects ..............'
				withMaven(maven : 'maven_3_6_0'){
					sh 'mvn package'
				}
			}
		}
		
		stage('Stage: Deploy in WAS') {
			steps {
				echo 'Deploying in WAS ..............'
				build job: 'DeployToWAS', parameters: [string(name: 'WAR_LOC', value: 'PipelineByAlakD/target/*.war'), string(name: 'APP_NAME', value: 'SampleWebApplication')]
			}
		}
    }
}

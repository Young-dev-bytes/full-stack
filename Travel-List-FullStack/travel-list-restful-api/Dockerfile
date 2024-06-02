FROM maven As backend-build
WORKDIR /fullstack/backend
COPY pom.xml .
RUN mvn dependency:go-offline -B

COPY src src
RUN mvn clean package -DskipTests

COPY code-server-4.89.0-linux-amd64.tar.gz /fullstack/backend

FROM openjdk:17-jdk-alpine
WORKDIR /young

COPY --from=backend-build /fullstack/backend/target/*.jar /young/app.jar
COPY --from=backend-build /fullstack/backend/code-server-4.89.0-linux-amd64.tar.gz /young/code-server/

RUN mkdir -p /young/code-server && tar -zxvf /young/code-server/code-server-4.89.0-linux-amd64.tar.gz -C /young/code-server

ENTRYPOINT ["sh","-c","java -jar app.jar"]
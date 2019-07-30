# airflow_learning
   - Hello world Reference: 
       - https://ohke.hateblo.jp/entry/2018/04/21/230000
       - https://github.com/puckel/docker-airflow

   - Use password_auth:
     - Enviroment parameters should be set.
        ```
        - AIRFLOW__WEBSERVER__AUTHENTICATE=True`
        - AIRFLOW__WEBSERVER__AUTH_BACKEND=airflow.contrib.auth.backends.password_auth
        ```
     - Use the Dockerfile and config file from https://github.com/puckel/docker-airflow
     - Build:
       ```
       docker build --rm --build-arg AIRFLOW_DEPS="datadog,dask" --build-arg PYTHON_DEPS="flask_oauthlib>=0.9" -t puckel/docker-airflow .
       ```
     - Up the containers:
       ```
       docker-compose -f docker-compose-CeleryExecutor.yml up -d
       ```
     - Set the user and password
       - Create Password hash:
          ```
          docker exec -it <webserver container name> python`
          >>> from flask_bcrypt import generate_password_hash`
          >>> generate_password_hash('your_password')`
          ```
       - Create user:(superuser)
          ```
          docker exec -it <postgres container name> psql -U airflow`
          airflow=# \connect airflow`
          insert into users values (<id>, <user>, <email>, <hased_password_value>, <superuser>);
          ```
       - Reference: https://github.com/puckel/docker-airflow/issues/201  

       

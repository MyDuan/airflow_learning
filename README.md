# airflow_learning
   - Hello world Reference: 
       - https://ohke.hateblo.jp/entry/2018/04/21/230000
       - https://github.com/puckel/docker-airflow

   - Run in local:
     - In docker-compose-CeleryExecutor.yml the enviroment parameters should be set. (I did it)
        ```
        - AIRFLOW__WEBSERVER__AUTHENTICATE=True`
        - AIRFLOW__WEBSERVER__AUTH_BACKEND=airflow.contrib.auth.backends.password_auth
        ```
     - Run:
       ```
       docker build --rm --build-arg AIRFLOW_DEPS="datadog,dask" --build-arg PYTHON_DEPS="flask_oauthlib>=0.9" -t puckel/docker-airflow .
       ```
     - Run:
       ```
       docker-compose -f docker-compose-CeleryExecutor.yml up -d
       ```
         - URL: http://localhost:3100 (need login)
         
     - Set the user and password
       - Create Password hash:
          - run `docker exec -it <webserver container name> python`
              - for example: `docker exec -it airflow_learning_webserver_1 python`
          - run
              - `>>> from flask_bcrypt import generate_password_hash`
              - `>>> generate_password_hash('your_password')`
                  - for example: `>>> generate_password_hash('12345')`
                  - can get the hash: `b'$2b$12$T0zjLdB1aIEvk0m/NbmYM.Pw/uNxK2TLwR5X/rDe7Yb2YD.y66lm6'`
              - `>>> exit()`
       - Create user:(superuser)
          - run: `docker exec -it <postgres container name> psql -U airflow`
              - for example: `docker exec -it airflow_learning_postgres_1 psql -U airflow`
          - run:   
              - `airflow=# \connect airflow`
              - `insert into users values (<id>, <user>, <email>, <hased_password_value>, <superuser>);`
                  - for example: `insert into users values (1, 'user_1', '123@123.com', '$2b$12$T0zjLdB1aIEvk0m/NbmYM.Pw/uNxK2TLwR5X/rDe7Yb2YD.y66lm6', true);`
       - In http://localhost:3100 , can login and see the main page.
       - Reference: https://github.com/puckel/docker-airflow/issues/201  

       

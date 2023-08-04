import logging
import pandas as pd
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from users.models import CustomUser
from casamento.models import UserUpload
from casamento.serializers import UserUploadSerializer
from users.constants import USER_TYPE


logger = logging.getLogger(__name__)

class UserUploadViewSet(viewsets.ModelViewSet):

    queryset = UserUpload.objects.all()
    serializer_class = UserUploadSerializer

    def perform_create(self, serializer):
        upload = serializer.save()
        logger.info(f'Upload created with id: {upload.id}') 

        df = pd.read_excel(upload.upload.path)
        logger.info(f'{len(df)} rows read from Excel file')

        required_columns = ['email', 'name', 'user_type']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            raise ValidationError(f"The following columns are missing from the worksheet: {', '.join(missing_columns)}")

        error_log = []
        for index, row in df.iterrows():
            try:
                email = row['email'].lower().strip()
                name = ' '.join([word.capitalize() for word in row['name'].split()])
                user_type = row['user_type'].strip()

                if user_type not in [choice[0] for choice in USER_TYPE]:
                    raise ValidationError(f"Invalid User Type: {user_type}")

                if CustomUser.objects.filter(email=email).exists():
                    logger.warning(f"User with email {email} already exists.")
                    error_log.append(f"User with email {email} already exists.")
                    continue
                    
                password = 'user123' 
                logger.info(f'About to create user with email {email}')
                CustomUser.objects.create_user(
                    email=email,
                    name=name,
                    password=password,
                    user_type=user_type,
                )
                logger.info(f'Successfully created user with email {email}')
            except Exception as e:
                logger.error(f'Error creating user {email}: {e}')
                error_log.append(str(e))

        if error_log:
            logger.error(f'The following errors occurred during user creation: {error_log}')

from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash():

    @staticmethod
    def bcrypt(password: str):
        """
        Método para encriptar una string, usado para cifrar la contraseña

        Args:
            password (str): [description]

        Returns:
            [type]: [description]
        """
        return pwd_cxt.hash(password)

    @staticmethod
    def verify(hashed_password, plain_password):
        """
        Metodo para verificar el empalme de la constraseña hasheada con 
        la constraseña en texto plano.

        Args:
            hashed_password (bool): [description]
            plain_password ([type]): [description]

        Returns:
            [type]: [description]
        """
        return pwd_cxt.verify(plain_password, hashed_password)

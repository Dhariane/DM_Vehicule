import axios from 'axios';
import Cookies from 'js-cookie';

const vehicule_api = process.env.NEXT_PUBLIC_VEHICULE_API || '';
const vehicule_admin = process.env.NEXT_PUBLIC_VEHICULE_ADMIN || '';
interface LoginResult {
  status: number;
  success?: boolean;
  message?: string;  
}

interface RegisterResult {
  status: number;
  success: boolean;
  message: string;
}

export const adminLogin = async (
  username: string,
  password: string,
): Promise<LoginResult> => {
  try {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await axios.post<{ access: string; refresh: string }>(
      `${vehicule_api}/auth/admin/login/`, 
      formData, 
      { headers: { 'Content-Type': 'multipart/form-data' } }
    );

    const data = response.data;

    Cookies.set("access_token", data.access, { 
      expires: 1, 
      secure: process.env.NODE_ENV === 'production' 
    });
    Cookies.set("refresh_token", data.refresh, { expires: 1, secure: process.env.NODE_ENV === 'production' });

    
    return { status: 200, success: true };

  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      const status = error.response.status;
      const data = error.response.data;

      if (status === 400) {
        return {
          status,
          success: false,
          message: data.message || "l'adresse e-mail ou mot de passe incorrect",
        };
      }
      return {
        status: 404,
        success: false,
        message: data.message || "Identifiants introuvable",
      };
    }
    return { status: 500, success: false, message: "serveur RH inaccessible" };
  }
};

export const login = async (
  username: string,
  password: string,
): Promise<LoginResult> => {
  try {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await axios.post<{ access: string; refresh: string }>(
      `${vehicule_api}/auth/login/`, 
      formData, 
      { headers: { 'Content-Type': 'multipart/form-data' } }
    );

    const data = response.data;

    Cookies.set("access_token", data.access, { expires: 1, secure: process.env.NODE_ENV === 'production' });
    Cookies.set("refresh_token", data.refresh, { expires: 1, secure: process.env.NODE_ENV === 'production' });
    
    return { status: 200, success: true };

  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      const status = error.response.status;
      const data = error.response.data;

      if (status === 404) {
        return {
          message: "identifiants publique introuvable",
          success: false,
          status: 404
        };
      }
      return {
        status,
        success: false,
        message: data.message || "l'adresse e-mail publique ou mot de passe incorrect",
      };
    }
    return { status: 500, success: false, message: "serveur publique inaccessible" };
  }
};

export const adminRegister = async (
  username: string,
  password: string,
  email: string,
  nom: string,
  prenom: string,
): Promise<RegisterResult> => {
  try {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('email', email);
    formData.append('password', password);
    formData.append('nom', nom);
    formData.append('prenom', prenom);

    await axios.post(
      `${vehicule_api}/demandeurs/`, 
      formData, 
      { headers: { 'Content-Type': 'multipart/form-data' } }
    );

    return { status: 201, success: true, message: "Profil enregistré" };

  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      const status = error.response.status;
      const result = error.response.data;


      return {
        status: status,
        success: false,
        message: result.message,
      };
    }
    return { status: 500, success: false, message: "Erreur de connexion au serveur" };
  }
};
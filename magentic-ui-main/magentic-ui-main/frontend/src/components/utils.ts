import { RcFile } from "antd/es/upload";
import { IStatus } from "./types/app";

export const getServerUrl = () => {
  const apiUrl = process.env.GATSBY_API_URL || "/api";
  console.log("GATSBY_API_URL:", process.env.GATSBY_API_URL);
  console.log("Using API URL:", apiUrl);
  return apiUrl;
};

export function setCookie(name: string, value: any, days: number) {
  let expires = "";
  if (days) {
    const date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
    expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

export function getCookie(name: string) {
  const nameEQ = name + "=";
  const ca = document.cookie.split(";");
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == " ") c = c.substring(1, c.length);
    if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
  }
  return null;
}
export function setLocalStorage(
  name: string,
  value: any,
  stringify: boolean = true
) {
  if (stringify) {
    localStorage.setItem(name, JSON.stringify(value));
  } else {
    localStorage.setItem(name, value);
  }
}

export function getLocalStorage(name: string, stringify: boolean = true): any {
  if (typeof window !== "undefined") {
    const value = localStorage.getItem(name);
    try {
      if (stringify) {
        return JSON.parse(value!);
      } else {
        return value;
      }
    } catch (e) {
      return null;
    }
  } else {
    return null;
  }
}

export function fetchJSON(
  url: string | URL,
  payload: any = {},
  onSuccess: (data: any) => void,
  onError: (error: IStatus) => void,
  onFinal: () => void = () => {}
) {
  return fetch(url, payload)
    .then(function (response) {
      if (response.status !== 200) {
        console.log(
          "Looks like there was a problem. Status Code: " + response.status,
          response
        );
        response.json().then(function (data) {
          console.log("Error data", data);
        });
        onError({
          status: false,
          message:
            "Connection error " + response.status + " " + response.statusText,
        });
        return;
      }
      return response.json().then(function (data) {
        onSuccess(data);
      });
    })
    .catch(function (err) {
      console.log("Fetch Error :-S", err);
      onError({
        status: false,
        message: `There was an error connecting to server. (${err}) `,
      });
    })
    .finally(() => {
      onFinal();
    });
}

export function eraseCookie(name: string) {
  document.cookie = name + "=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;";
}

export function truncateText(text: string, length = 50) {
  if (text.length > length) {
    return text.substring(0, length) + " ...";
  }
  return text;
}

export const fetchVersion = () => {
  const versionUrl = getServerUrl() + "/version";
  return fetch(versionUrl)
    .then((response) => response.json())
    .then((data) => {
      return data;
    })
    .catch((error) => {
      console.error("Error:", error);
      return null;
    });
};

export const convertFilesToBase64 = async (files: RcFile[] = []) => {
  return Promise.all(
    files.map(async (file) => {
      return new Promise<{ name: string; content: string; type: string }>(
        (resolve, reject) => {
          const reader = new FileReader();
          reader.onload = () => {
            // Extract base64 content from reader result
            const base64Content = reader.result as string;
            // Remove the data URL prefix (e.g., "data:image/png;base64,")
            const base64Data = base64Content.split(",")[1] || base64Content;
            resolve({ name: file.name, content: base64Data, type: file.type });
          };
          reader.onerror = reject;
          reader.readAsDataURL(file);
        }
      );
    })
  );
};

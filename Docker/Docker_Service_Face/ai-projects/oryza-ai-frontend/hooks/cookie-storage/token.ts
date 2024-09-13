import Cookies from "js-cookie";

export default class TokenCookieStore {
  private REFESH_TOKEN = process.env.NEXT_PUBLIC_REFESH_TOKEN_NAME as string;
  private ACCESS_TOKEN = process.env.NEXT_PUBLIC_ACCESS_TOKEN_NAME as string;
  private domain = process.env.NEXT_PUBLIC_DOMAIN;

  private static instance: TokenCookieStore;

  public static getInstance(): TokenCookieStore {
    if (!TokenCookieStore.instance) {
      TokenCookieStore.instance = new TokenCookieStore();
    }
    return TokenCookieStore.instance;
  }

  constructor() {}

  public get_access_token() {
    return Cookies.get(this.ACCESS_TOKEN);
  }

  public set_access_token(value: string, expired: number) {
    Cookies.set(this.ACCESS_TOKEN, value, {
      expires: new Date(expired),
      path: "/",
      domain: this.domain ? this.domain : "",
      sameSite: "Lax",
    });
  }

  public remove_access_token() {
    Cookies.remove(this.ACCESS_TOKEN, {
      domain: this.domain ? this.domain : "",
      path: "/",
    });
  }

  public get_refresh_token() {
    return Cookies.get(this.REFESH_TOKEN);
  }

  public set_refresh_token(value: string, expired: number) {
    Cookies.set(this.REFESH_TOKEN, value, {
      expires: new Date(expired),
      path: "/",
      domain: this.domain ? this.domain : "",
      sameSite: "Lax",
    });
  }

  public remove_refresh_token() {
    Cookies.remove(this.REFESH_TOKEN, {
      domain: this.domain ? this.domain : "",
      path: "/",
    });
  }
}

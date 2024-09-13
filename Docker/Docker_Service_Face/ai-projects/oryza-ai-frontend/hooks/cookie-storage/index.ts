import TokenCookieStore from "./token";

export class CookieStoreControl {
  private static instance: CookieStoreControl;
  public token: TokenCookieStore = TokenCookieStore.getInstance();

  private constructor() {}

  public static getInstance(): CookieStoreControl {
    if (!CookieStoreControl.instance) {
      CookieStoreControl.instance = new CookieStoreControl();
    }

    return CookieStoreControl.instance;
  }
}

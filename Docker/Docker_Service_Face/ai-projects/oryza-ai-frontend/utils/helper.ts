export const changeTheme = (value: string) => {
  document.querySelector("html")?.setAttribute("data-theme", value);
};

import { TextFieldForm, Button100 } from "@/components/common";
import { useAuth } from "@/hooks/auth-hook";
import { FormState } from "@/interfaces/common";
import { Validator } from "@/utils";
import { useRouter } from "next/navigation";
import * as React from "react";
import { useState } from "react";
import { enqueueSnackbar } from "notistack";

export interface ILoginFormProps {}

export function LoginForm(props: ILoginFormProps) {
  const { login } = useAuth();

  const router = useRouter();
  const [formState, setFormState] = useState<FormState>("NONE");

  const [formError, setFormError] = useState<any>({
    email: null,
    password: null,
  });

  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (formState === "LOADING") return;

    const formData = new FormData(event.currentTarget);

    const form_values = Object.fromEntries(formData);

    if (validate(form_values)) return;
    setFormState("LOADING");
    try {
      let payload = {
        password: form_values.password.toString(),
        username: form_values.email.toString(),
      };
      await login(payload);
      enqueueSnackbar("Đăng nhập thành công", { variant: "success" });
      router.replace("/manage");
    } catch (error) {
      enqueueSnackbar("Đăng nhập không thành công", { variant: "error" });
    } finally {
      setFormState("SUCCESS");
    }
  }

  function validate(data: any) {
    // Destructure input data
    const { email, password } = data;
    let hasError = false;

    // Object to store validation errors
    let error = {
      email: Validator.checkNotEmpty(email), // Check if email is valid
      password: Validator.checkNotEmpty(password), // Check if password is not empty
    };

    // If any validation error exists, set hasError to true
    if (error.password !== null) {
      hasError = true;
    }

    // Set form error state
    setFormError(error);

    return hasError; // Return whether there are validation errors
  }

  return (
    <div className="items-center flex flex-col space-y-[32px] ">
      <h1 className="font-title text-[#007dc0] text-2xl font-normal">
        ĐĂNG NHẬP
      </h1>
      <form
        onSubmit={onSubmit}
        action=""
        className="flex flex-col min-w-[350px]"
      >
        <TextFieldForm
          lable={"Email"}
          name="email"
          placeholder="example@oryza.vn"
          textError={formError.email}
          defaultValue={process.env.NODE_ENV === "development" ? "admin" : ""}
        />
        <br />
        <TextFieldForm
          lable={"Mật khẩu"}
          name="password"
          type="password"
          placeholder="Nhập mật khẩu..."
          textError={formError.password}
          defaultValue={process.env.NODE_ENV === "development" ? "1" : ""}
        />
        <p className="text-[#007DC0] text-sm font-normal cursor-pointer select-none mt-[8px]">
          Quên mật khẩu?
        </p>
        <Button100
          text={"Đăng nhập"}
          disabled={formState === "LOADING"}
          className={
            "bg-primary active:bg-[#026DA6] hover:bg-[#026DA6] text-white text-base	font-medium mt-[32px]"
          }
        />
      </form>
    </div>
  );
}

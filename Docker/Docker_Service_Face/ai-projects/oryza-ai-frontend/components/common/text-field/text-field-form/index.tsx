import * as React from "react";
import styles from "./styles.module.css";
import Icon from "../../icon";
import { useState } from "react";

export interface ITextFieldFormProps {
  lable: string;
  type?: React.HTMLInputTypeAttribute | undefined;
  name?: string;
  placeholder?: string | undefined;
  textError?: string;
  defaultValue?: string | undefined;
}

export function TextFieldForm(props: ITextFieldFormProps) {
  const { lable, type, name, placeholder, textError, defaultValue } = props;
  const isPassword = type === "password";
  const [showPw, setShowPw] = useState(false);
  const togglePassword = () => {
    setShowPw(!showPw);
  };
  return (
    <fieldset
      className={`${styles.textfield} ${textError && styles.textfieldError}`}
    >
      <label
        htmlFor={name}
        className={`${styles.label} ${textError && styles.labelError}`}
      >
        {lable}
      </label>
      <input
        type={showPw ? "text" : type}
        name={name}
        id={name}
        defaultValue={defaultValue}
        className={`${styles.input} ${
          textError && styles.inputError
        } px-[24px] py-[15px] ${isPassword && "pr-[40px]"}`}
        placeholder={placeholder}
        autoComplete="off"
      />
      {textError && <p className={styles.helperText}>{textError}</p>}

      {isPassword && (
        <div
          onClick={togglePassword}
          className={textError ? styles.eyeError : styles.eye}
        >
          <Icon name={!showPw ? "eye-off" : "eye-on"} />
        </div>
      )}
    </fieldset>
  );
}

import { ResultEnum } from "@/constants/enum";
import { useState } from "react";

type FormDataObject = {
  [key: string]: string | Blob;
};
type SubmitFunction = (formData: FormDataObject) => Promise<ResultEnum>;

type ValidateFunction = (formData: FormDataObject) => boolean;

const useFormSubmit = (
  submitFunction: SubmitFunction,
  validateFunction: ValidateFunction
) => {
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const formJson = Object.fromEntries(formData.entries());
    if (!validateFunction(formJson)) return;
    setLoading(true);
    // await delaySubmit();
    let result = await submitFunction(formJson);
    setLoading(false);
    return result;
  };

  return { loading, handleSubmit };
};
function delaySubmit() {
  return new Promise((resolve, reject) => {
    setTimeout(async () => {
      try {
        resolve("hehe");
      } catch (error) {
        reject(error);
      }
    }, 500);
  });
}
export default useFormSubmit;

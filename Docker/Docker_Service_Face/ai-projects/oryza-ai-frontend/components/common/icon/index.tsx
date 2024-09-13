import clsx from "clsx";
import LoadingSVG from "@/assets/svgs/linea-arrows-rotate.svg";
import useDynamicIconImport from "@/hooks/use-icon";

type TProps = {
  name: string;
  className?: string;
};

const Icon = ({ name, className, ...rest }: TProps) => {
  const { loading, error, SvgIcon } = useDynamicIconImport(name);

  if (error) {
    return null;
  }

  if (loading) {
    return <LoadingSVG className={clsx(className)} />;
  }

  if (SvgIcon) {
    return <SvgIcon className={clsx(className)} {...rest} />;
  }

  return null;
};

export default Icon;

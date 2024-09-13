import { FC, ReactNode, UIEventHandler } from "react";
import PropTypes from "prop-types";
import { Scrollbars } from "react-custom-scrollbars-2";

interface ScrollbarProps {
  className?: string;
  children?: ReactNode;
  autoHide?: boolean | undefined;
  onScroll?: UIEventHandler<any> | undefined;
}

const Scrollbar: FC<ScrollbarProps> = ({
  className,
  children,
  onScroll,
  autoHide,
  ...rest
}) => {
  return (
    <Scrollbars
      autoHide
      universal
      onScroll={onScroll}
      className={className}
      renderThumbVertical={() => {
        return (
          <div
            style={{
              width: 5,
              background: `#55595d50`,
              borderRadius: "4px",
              transition: "background .3s",
            }}
          />
        );
      }}
      {...rest}
    >
      {children}
    </Scrollbars>
  );
};

Scrollbar.propTypes = {
  children: PropTypes.node,
  className: PropTypes.string,
};

export default Scrollbar;

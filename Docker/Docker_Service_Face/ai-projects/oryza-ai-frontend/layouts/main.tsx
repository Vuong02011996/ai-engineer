import * as React from "react";

export interface IMainLayoutProps {
  children: React.ReactNode;
}

export default function MainLayout({ children }: IMainLayoutProps) {
  return (
    <div className="tw-bg-red-200 tw-w-screen tw-h-scree">
      <div>{children}</div>
    </div>
  );
}

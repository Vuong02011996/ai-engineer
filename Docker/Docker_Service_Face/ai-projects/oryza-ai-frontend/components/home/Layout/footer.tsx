const Footer = () => {
  return (
    <div className="bg-white-300 pt-44 pb-24">
      <div className="max-w-screen-xl w-full mx-auto px-6 sm:px-8 lg:px-16 grid grid-rows-6 sm:grid-rows-1 grid-flow-row sm:grid-flow-col grid-cols-3 sm:grid-cols-12 gap-4">
        <div className="row-span-2 sm:col-span-4 col-start-1 col-end-4 sm:col-end-5 flex flex-col items-start ">
          <img
            src="/assets/logo-white.svg"
            alt=""
            className="h-8 w-auto mb-6"
          />
          <p className="mb-4 text-white">
            <strong className="font-medium">Oryza AI</strong> cung cấp các tính
            năng AI tiên tiến cho camera an ninh, từ nhận diện khuôn mặt đến
            giám sát đám đông, giúp bảo vệ và quản lý an ninh một cách thông
            minh và hiệu quả.
          </p>
          <div className="flex w-full mt-2 mb-8 -mx-2">
            <div className="mx-2 bg-white-500 rounded-full items-center justify-center flex p-2 shadow-md">
              <a
                href="https://www.facebook.com/OryzaSystems.Official"
                target="_blank"
              >
                <img
                  src="/assets/Icon/facebook.svg"
                  alt="facebook"
                  className="h-6 w-6"
                />
              </a>
            </div>
            <div className="mx-2 bg-white-500 rounded-full items-center justify-center flex p-2 shadow-md">
              <a href="https://www.youtube.com/@OryzaSystems" target="_blank">
                <img
                  src="/assets/Icon/twitter.svg"
                  alt="twitter"
                  className="h-6 w-6"
                />
              </a>
            </div>
            <div className="mx-2 bg-white-500 rounded-full items-center justify-center flex p-2 shadow-md">
              <a
                href="https://www.linkedin.com/company/oryzasystems/"
                target="_blank"
              >
                <img
                  src="/assets/Icon/instagram.svg"
                  alt="instagram"
                  className="h-6 w-6"
                />
              </a>
            </div>
          </div>
          <p className="text-gray-400">
            ©{new Date().getFullYear()} - Oryza AI
          </p>
        </div>
        <div className=" row-span-2 sm:col-span-2 sm:col-start-7 sm:col-end-9 flex flex-col">
          <p className="text-white mb-4 font-medium text-lg">Sản phẩm</p>
          <ul className="text-white ">
            <a href="https://product.oryzacloud.vn/" target="_blank">
              <li className="my-2 hover:text-[#007dc0] cursor-pointer transition-all ">
                Hệ sinh thái IoT
              </li>
            </a>
            <a href="https://product.oryzacloud.vn/" target="_blank">
              <li className="my-2 hover:text-[#007dc0] cursor-pointer transition-all">
                Hệ sinh thái Oryza ERP
              </li>
            </a>
            <a href="https://product.oryzacloud.vn/" target="_blank">
              <li className="my-2 hover:text-[#007dc0] cursor-pointer transition-all">
                An toàn thông tin
              </li>
            </a>
            <a href="https://oryza.vn/san-pham/oryza-vms" target="_blank">
              <li className="my-2 hover:text-[#007dc0] cursor-pointer transition-all">
                Oryza VMS
              </li>
            </a>
          </ul>
        </div>
        <div className="row-span-2 sm:col-span-2 sm:col-start-9 sm:col-end-11 flex flex-col">
          <p className="text-white mb-4 font-medium text-lg">Giới thiệu</p>
          <ul className="text-white">
            <a href="https://oryza.vn/ve-cong-ty" target="_blank">
              <li className="my-2 hover:text-[#007dc0] cursor-pointer transition-all">
                Về công ty
              </li>
            </a>
            <a href="https://oryza.vn/ve-cong-ty" target="_blank">
              <li className="my-2 hover:text-[#007dc0] cursor-pointer transition-all">
                Tuyển dụng
              </li>
            </a>
            <a href="https://oryza.vn/tin-tuc?page=1" target="_blank">
              <li className="my-2 hover:text-[#007dc0] cursor-pointer transition-all">
                Tin tức
              </li>
            </a>
            <a href="https://oryza.vn/lien-he" target="_blank">
              <li className="my-2 hover:text-[#007dc0] cursor-pointer transition-all">
                Liên hệ
              </li>
            </a>
          </ul>
        </div>
        <div className="row-span-2 sm:col-span-2 sm:col-start-11 sm:col-end-13 flex flex-col">
          <p className="text-white mb-4 font-medium text-lg">Liên hệ</p>
          <ul className="text-white">
            <a href="https://oryza.vn/lien-he" target="_blank">
              <li className="my-2 hover:text-[#007dc0] cursor-pointer transition-all">
                Chăm sóc khách hàng
              </li>
            </a>
            <a href="https://oryza.vn/" target="_blank">
              <li className="my-2 hover:text-[#007dc0] cursor-pointer transition-all">
                oryza.vn
              </li>
            </a>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Footer;

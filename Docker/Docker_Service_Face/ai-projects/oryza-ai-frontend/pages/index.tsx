import { SeoPage } from "@/components/common";
import Layout from "@/components/home/Layout/layout";
import Feature from "@/components/home/feature";
import Hero from "@/components/home/hero";
import { homePageShema } from "@/constants/schema";

export interface IHomePageProps {}

export default function HomePage(props: IHomePageProps) {
  return (
    <>
      <SeoPage
        title="Oryza AI | Giải Pháp AI Toàn Diện Cho Chuyển Đổi Số An Ninh"
        description="Oryza AI cung cấp giải pháp AI toàn diện cho an ninh, bao gồm nhận diện khuôn mặt, phát hiện đồ vật bỏ rơi, nhận diện biển số, phát hiện đồng phục, giám sát người lảng vảng và phát hiện đám đông. Tối ưu hóa an ninh và quản lý với công nghệ AI tiên tiến."
        schema={homePageShema}
        imagePreview="/assets/camera-ai.png"
      />
      <Layout>
        <Hero />
        <Feature />
      </Layout>
    </>
  );
}

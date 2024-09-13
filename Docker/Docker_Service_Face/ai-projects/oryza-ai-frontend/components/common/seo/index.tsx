import { URL_PRODUCT } from "@/constants";
import { renderSchemaProduct } from "@/utils/global-func";
import Head from "next/head";
import { useRouter } from "next/router";

export interface SeoPageProps {
  title: string;
  description?: string;
  imagePreview?: string;
  ogTitle?: string;
  schema?: any[];
}

export function SeoPage(props: SeoPageProps) {
  const description =
    props?.description || "Công ty cổ phần công nghệ Oryza System";
  const image = props?.imagePreview || "/img-seo/Oryza-Systems.png";
  const ogTitle = props?.ogTitle || props.title;
  const title = props.title
    ? props.title + " - Oryza AI"
    : `${props.title || "Pages"} - Oryza JSC`;
  const router = useRouter();

  const canonical = `${URL_PRODUCT}${router.asPath}`;

  const renderSchema = () => {
    if (!props.schema) return;
    if (props.schema.length <= 0) {
      return (
        <script type="application/ld+json">
          {JSON.stringify(renderSchemaProduct(title))}
        </script>
      );
    }

    return props.schema.map((schema, index) => (
      <script key={index} type="application/ld+json">
        {JSON.stringify(schema)}
      </script>
    ));
  };

  return (
    <Head>
      <title>{title}</title>
      <meta name="description" content={description} />
      <meta property="og:image" content={image} />
      <meta property="og:image:url" content={image} />
      <meta property="og:image:secure_url" content={image} />
      <meta property="og:title" content={ogTitle} />
      <link rel="canonical" href={canonical} />
      {renderSchema()}
    </Head>
  );
}

import Head from "next/head";

const Seo = ({
  title = "Full-Stack App Boilerplate - Django, Next.js, Docker & PgBouncer",
  keywords = "Full-Stack Boilerplate, Django Next.js Docker, Docker Compose Full-Stack, PgBouncer Setup, Django with PgBouncer, Next.js Docker Dev Setup, Django REST Framework, Next.js Client with Django API, Dockerized Full-Stack App, Full-Stack Dev Starter Kit, Django Redis Celery, Django PostgreSQL PgBouncer, Next.js .env config, Scalable Full-Stack Architecture, System Design Starter Project, Django Flower Monitor, DevOps with Django and Next.js, Modern Full-Stack Template, Python Backend with React Frontend, Django Docker Postgres Setup, Full-Stack App with Authentication, Environment Configuration for Full-Stack, Reusable Full-Stack Template",
  description = `A modern and production-ready full-stack boilerplate using Django (API), Next.js (client), Docker, PgBouncer, Redis, and Celery. Ideal for building scalable and well-architected applications with best practices in DevOps and modular development.`,
  imagePreview = "https://techtipsbymoh.tor1.cdn.digitaloceanspaces.com/general/Web%20Cover%20Photo-new.png",
  url = "https://tipsbymoh.tech/",
  imgAlt = "",
  hidden_to_search_engines = false,
  structuredData = {},
  children,
}) => {
  return (
    <>
      <Head>
        <title>{title}</title>
        <link rel="canonical" href={url} />
        <meta name="description" content={description} />
        <meta
          name="keywords"
          content={`${keywords}, Tech Tips, Tech Tips By Moh`}
        />
        <meta property="og:title" content={title} />
        <meta property="og:description" content={description} />
        <meta property="og:image" content={imagePreview} />
        <meta property="og:url" content={url} />
        <meta property="og:type" content="website" />
        <meta property="og:site_name" content="Tech Tips By Moh" />
        <meta name="twitter:card" content={imgAlt || title} />
        <meta name="twitter:title" content={title} />
        <meta name="twitter:description" content={description} />
        <meta name="twitter:image" content={imagePreview} />
        <meta name="twitter:url" content={url} />
        {hidden_to_search_engines ? (
          <meta name="robots" content="noindex,nofollow,noarchive" />
        ) : (
          ""
        )}
        {Object.keys(structuredData)?.length ? (
          <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
          />
        ) : (
          ""
        )}
      </Head>
      {children}
    </>
  );
};

export default Seo;

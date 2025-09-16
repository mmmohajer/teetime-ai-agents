import Seo from "@/components/wrappers/Seo";
import NotFound from "@/components/publicWebPages/NotFound";

const index = () => {
  return (
    <>
      <Seo
        title="Page Not Found | Tech Tips by Moh"
        keywords="404 Error, Page Not Found, Tech Tips, Web Development, Coding Tips, Software Engineering"
        description="Oops! The page you're looking for isn't here. Explore the latest tech insights, coding tips, and system design strategies on Tech Tips by Moh."
      >
        <NotFound />
      </Seo>
    </>
  );
};

export default index;

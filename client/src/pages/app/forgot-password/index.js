import Seo from "@/components/wrappers/Seo";
import AppContainer from "@/components/wrappers/AppContainer";
import ForgotPassword from "@/components/appPages/ForgotPassword";

const Index = () => {
  return (
    <Seo
      title="Tech Tips by Moh | Forgot Your Password"
      keywords="Full-Stack Developer, System Design, Software Engineer, Tech Mentor, AI, DevOps, Programming, Coding Tips"
      description="Expert coding tips and full-stack strategies by Mohammad Mahdi Mohajer at Tech Tips By Moh. Ideal for devs, SaaS founders, and startups. Book a free call."
      imagePreview="https://techtipsbymoh.tor1.cdn.digitaloceanspaces.com/general/Web%20Cover%20Photo-new.png"
      url="https://tipsbymoh.tech/app/forgot-password"
      imgAlt="Tech Tips by Moh | Full-Stack Developer, System Design Expert, and Tech Mentor"
    >
      <AppContainer isAuthPage={true} pageIdentifier="forgot-password">
        <ForgotPassword />
      </AppContainer>
    </Seo>
  );
};

export default Index;

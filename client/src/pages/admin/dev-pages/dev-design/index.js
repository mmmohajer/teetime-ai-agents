import Seo from "@/components/wrappers/Seo";
import PageContainer from "@/components/wrappers/PageContainer";
import AppContainer from "@/components/wrappers/AppContainer";
import DevDesign from "@/components/DevPages/DevDesign";

const Index = () => {
  return (
    <>
      <Seo hidden_to_search_engines={true}>
        <AppContainer pageIdentifier="dev-page" hasSideBarDashboard={false}>
          <DevDesign />
        </AppContainer>
      </Seo>
    </>
  );
};

export default Index;

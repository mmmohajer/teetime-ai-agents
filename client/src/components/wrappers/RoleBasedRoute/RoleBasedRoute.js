import { useSelector } from "react-redux";

import Div from "@/baseComponents/reusableComponents/Div";

const RoleBasedRoute = ({ authorizedRoles, children }) => {
  const profile = useSelector((state) => state.profile);
  return (
    <>
      {profile?.user?.groups?.some((item) =>
        authorizedRoles?.includes(item)
      ) ? (
        children
      ) : profile?.user?.groups?.length ? (
        <Div
          type="flex"
          hAlign="center"
          vAlign="center"
          className="pos-fix pos-fix--lt width-per-100 height-vh-full bg-white"
          style={{ zIndex: 100000000000 }}
        >
          <Div className="width-per-100 max-width-px-700 text-center bg-red text-white p-all-temp-7 br-rad-px-10">
            This is a restricted area. You do not have permission to access this
            content.
          </Div>
        </Div>
      ) : (
        ""
      )}
    </>
  );
};

export default RoleBasedRoute;

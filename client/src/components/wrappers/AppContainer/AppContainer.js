import cx from "classnames";
import { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";

import Div from "@/baseComponents/reusableComponents/Div/Div";
import Modal from "@/baseComponents/pageParts/Modal";
import Loading from "@/baseComponents/pageParts/Loading";
import Alert from "@/baseComponents/pageParts/Alert";
import AppHeader from "@/baseComponents/pageParts/AppHeader";
import SideBarDashboard from "@/baseComponents/pageParts/SideBarDashboard";
import FooterNavigation from "@/baseComponents/pageParts/FooterNavigation";
import BaseAppWrapper from "@/components/wrappers/BaseAppWrapper";

import useDivWidth from "@/hooks/useDivWidth";
import { hideMobNav } from "@/reducer/subs/isMobNavVisible";
import { setActiveMenu } from "@/reducer/subs/activeMenu";

const AppContainer = ({
  pageIdentifier,
  isAuthPage = false,
  hasSideBarDashboard = true,
  hasHeader = true,
  hasFooterNavigation = true,
  children,
}) => {
  const dispatch = useDispatch();
  const { type: modalType } = useSelector((state) => state.modal);
  const isLoading = useSelector((state) => state.isLoading);
  const alert = useSelector((state) => state.alert);

  const { containerRef, width } = useDivWidth();

  useEffect(() => {
    dispatch(hideMobNav());
  }, []);

  useEffect(() => {
    if (pageIdentifier) {
      dispatch(setActiveMenu(pageIdentifier));
    }
  }, [pageIdentifier]);

  return (
    <>
      <BaseAppWrapper isAuthPage={isAuthPage}>
        {isLoading ? <Loading /> : ""}
        {modalType ? <Modal /> : ""}
        {alert?.length ? <Alert /> : ""}
        <Div className="width-per-100 bg-theme-one min-height-vh-full">
          <Div
            ref={containerRef}
            className={cx(
              "width-per-100 global-container bg-white min-height-vh-full"
            )}
          >
            {width >= 800 ? (
              <Div type="flex">
                {hasSideBarDashboard && !isAuthPage ? <SideBarDashboard /> : ""}
                <Div
                  type="flex"
                  direction="vertical"
                  className="flex--gr--1 height-vh-full of-y-auto"
                >
                  {hasHeader && <AppHeader />}
                  {children}
                </Div>
              </Div>
            ) : (
              <Div type="flex" direction="vertical" className="height-vh-full">
                <Div
                  type="flex"
                  direction="vertical"
                  className={cx(
                    "flex--gr--1 of-y-auto",
                    hasSideBarDashboard ? "m-b-16" : ""
                  )}
                >
                  {hasHeader && <AppHeader />}
                  {children}
                </Div>
                {hasSideBarDashboard && !isAuthPage ? <FooterNavigation /> : ""}
              </Div>
            )}
          </Div>
        </Div>
      </BaseAppWrapper>
    </>
  );
};

export default AppContainer;

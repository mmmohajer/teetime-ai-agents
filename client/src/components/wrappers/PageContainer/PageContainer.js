import cx from "classnames";
import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";

import Div from "@/baseComponents/reusableComponents/Div/Div";
import Header from "@/baseComponents/pageParts/Header";
import Modal from "@/baseComponents/pageParts/Modal";
import Alert from "@/baseComponents/pageParts/Alert";
import Loading from "@/baseComponents/pageParts/Loading";
import Footer from "@/baseComponents/pageParts/Footer";

import useDivWidth from "@/hooks/useDivWidth";
import { hideMobNav } from "@/reducer/subs/isMobNavVisible";
import { setActiveMenu } from "@/reducer/subs/activeMenu";
import { setActiveSubMenuItem } from "@/reducer/subs/activeSubMenuItem";

const PageContainer = ({
  pageIdentifier,
  pageSubNavIdentifier,
  hasHeader = true,
  hasFooter = true,
  children,
}) => {
  const dispatch = useDispatch();
  const { containerRef, width } = useDivWidth(true);
  const { type: modalType } = useSelector((state) => state.modal);
  const isLoading = useSelector((state) => state.isLoading);
  const alert = useSelector((state) => state.alert);

  useEffect(() => {
    dispatch(hideMobNav());
  }, []);

  useEffect(() => {
    if (pageIdentifier) {
      dispatch(setActiveMenu(pageIdentifier));
    }
  }, [pageIdentifier]);

  useEffect(() => {
    if (pageSubNavIdentifier) {
      dispatch(setActiveSubMenuItem(pageSubNavIdentifier));
    } else {
      dispatch(setActiveSubMenuItem(""));
    }
  }, [pageSubNavIdentifier]);

  return (
    <>
      {isLoading ? <Loading /> : ""}
      {modalType ? <Modal /> : ""}
      {alert?.length ? <Alert /> : ""}
      <Div type="flex" direction="vertical" className="min-height-vh-full">
        {hasHeader ? <Header /> : null}
        <Div
          ref={containerRef}
          type="flex"
          direction="vertical"
          className={cx("width-per-100 flex--gr--1")}
        >
          {children}
        </Div>
        {hasFooter ? <Footer /> : null}
      </Div>
    </>
  );
};

export default PageContainer;

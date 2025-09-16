import { useMemo } from "react";
import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";

import useDivWidth from "@/hooks/useDivWidth";

const Table = ({
  headingTitleRows,
  headingData,
  bodyData,
  useFullWidth = true,
  className,
}) => {
  const { containerRef, width } = useDivWidth();

  const colWidths = useMemo(() => {
    if (!headingData?.length) return [];
    const baseWidths = headingData.map((col) => col?.width);
    const totalBaseWidth = baseWidths.reduce((a, b) => a + b, 0);
    if (useFullWidth && width && totalBaseWidth < width) {
      const stretchWidth = width / baseWidths.length;
      return baseWidths.map(() => stretchWidth);
    }
    return baseWidths;
  }, [headingData, useFullWidth, width]);

  const totalTableWidth = useMemo(() => {
    return colWidths.reduce((a, b) => a + b, 0);
  }, [colWidths]);

  return (
    <Div
      ref={containerRef}
      className={cx("width-per-100 of-x-auto scroll-type-one")}
    >
      <table
        style={{
          borderCollapse: "collapse",
          minWidth: `${totalTableWidth}px`,
        }}
        className={cx(className)}
      >
        <thead>
          <tr>
            {headingTitleRows?.map((col, colIdx) => (
              <th
                key={col?.identifier}
                colSpan={col?.colSpan || 1}
                rowSpan={col?.rowSpan || 1}
                style={{
                  width: `${colWidths
                    .slice(colIdx, colIdx + col?.colSpan || 1)
                    .reduce((a, b) => a + b, 0)}px`,
                  border: "1px solid black",
                }}
              >
                {col?.display}
              </th>
            ))}
          </tr>
          <tr>
            {headingData?.map((col, idx) =>
              col?.display !== null ? (
                <th
                  key={col?.identifier}
                  style={{
                    width: `${colWidths[idx]}px`,
                    border: "1px solid black",
                  }}
                >
                  {col?.display}
                </th>
              ) : null
            )}
          </tr>
        </thead>
        <tbody>
          {bodyData?.map((row, idx) => (
            <tr key={idx}>
              {headingData?.map((col, colIdx) => (
                <td
                  key={col?.identifier}
                  style={{
                    width: `${colWidths[colIdx]}px`,
                    border: "1px solid black",
                  }}
                >
                  {row[col?.identifier]?.display}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </Div>
  );
};

export default Table;

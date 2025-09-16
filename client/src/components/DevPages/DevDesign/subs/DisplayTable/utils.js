import Div from "@/baseComponents/reusableComponents/Div";

export const HEADING_TITLE_ROWS = () => [
  {
    identifier: "name",
    display: (
      <Div type="flex" hAlign="center" vAlign="center" className="bg-red">
        Name
      </Div>
    ),
    colSpan: 1,
  },
  {
    identifier: "userInfo",
    display: (
      <Div type="flex" hAlign="center" vAlign="center" className="bg-purple">
        User Info
      </Div>
    ),
    colSpan: 2,
  },
  {
    identifier: "email",
    display: (
      <Div type="flex" hAlign="center" vAlign="center" className="bg-orange">
        Email
      </Div>
    ),
    colSpan: 1,
    rowSpan: 2,
  },
];

export const HEADING_DATA = () => [
  {
    identifier: "name",
    name: "Name",
    display: (
      <Div type="flex" hAlign="center" vAlign="center" className="bg-green">
        Name
      </Div>
    ),
    width: 160,
  },
  {
    identifier: "city",
    name: "City",
    display: (
      <Div type="flex" hAlign="center" vAlign="center" className="bg-green">
        City
      </Div>
    ),
    width: 80,
  },
  {
    identifier: "age",
    name: "Age",
    display: (
      <Div type="flex" hAlign="center" vAlign="center" className="bg-green">
        Age
      </Div>
    ),
    width: 80,
  },
  {
    identifier: "email",
    display: null,
    width: 160,
  },
];

export const BODY_DATA = (MOCK_DATA) =>
  MOCK_DATA?.map((user) => ({
    name: {
      identifier: "name",
      value: user?.name,
      display: (
        <Div type="flex" hAlign="center" vAlign="center">
          {user?.name}
        </Div>
      ),
    },
    age: {
      identifier: "age",
      value: user?.age,
      display: (
        <Div type="flex" hAlign="center" vAlign="center">
          {user?.age}
        </Div>
      ),
    },
    city: {
      identifier: "city",
      value: user?.city,
      display: (
        <Div type="flex" hAlign="center" vAlign="center">
          {user?.city}
        </Div>
      ),
    },
    email: {
      identifier: "email",
      value: user?.email,
      display: (
        <Div type="flex" hAlign="center" vAlign="center">
          {user?.email}
        </Div>
      ),
    },
  }));

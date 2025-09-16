import { createSlice } from "@reduxjs/toolkit";

const reducerObject = {};
reducerObject["setModalType"] = (state, action) => {
  curState = { ...state };
  curState.type = action.payload;
  return curState;
};

reducerObject["setModalProps"] = (state, action) => {
  curState = { ...state };
  curState.props = action.payload;
  return curState;
};

reducerObject["setModal"] = (state, action) => action.payload;

reducerObject["clearModal"] = (state, action) => {
  return { type: "", props: {} };
};

const slice = createSlice({
  name: "modal",
  initialState: { type: "", props: {} },
  reducers: reducerObject,
});

export const { setModalType, setModalProps, setModal, clearModal } =
  slice.actions;
export default slice.reducer;

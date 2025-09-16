export const setLocalStorage = (key, value) => {
  if (localStorage) {
    localStorage.setItem(key, JSON.stringify(value));
  }
};

export const removeLocalStorage = (key) => {
  if (localStorage?.getItem(key)) {
    localStorage.removeItem(key);
  }
};

export const getLocalStorage = (key) => {
  if (localStorage && localStorage?.getItem(key)) {
    return JSON.parse(localStorage.getItem(key));
  }
  return "";
};

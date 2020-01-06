import React, { useContext } from "react";
import { store } from "./index";
import dayjs from "dayjs";

const formattedDay = day => {
  return dayjs(day).format("dddd, MMMM DD YYYY");
};

export const Date = () => {
  const { selected } = useContext(store);
  const txt = formattedDay(selected[0]);
  return <div className="date-display">{txt}</div>;
};

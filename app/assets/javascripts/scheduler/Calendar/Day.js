import React, { useContext, useRef, useEffect } from "react";
import {
  store,
  isBlockedDay,
  formattedDay,
  yearMonthDay,
  isSelected
} from "./index";

export const Day = ({ day }) => {
  const { today, selected, focusedDayNum, dispatch } = useContext(store);
  const { $D: dayNum = 0 } = day;
  const { $D: todayDayNum = 0 } = today;
  const tabIndex = dayNum !== todayDayNum ? { tabIndex: -1 } : {};
  const isDisabled = isBlockedDay(day, useContext(store));
  const isCurrent = day.isSame(today);
  const formattedDate = yearMonthDay(day);
  const pressed = isSelected(selected, formattedDate);
  const bthState = isDisabled
    ? "Calendar-item--unavailable"
    : "Calendar-item--active";
  const currentState = isCurrent ? { "aria-current": "date" } : {};
  const labelDate = formattedDay(day);
  const label = isDisabled ? `Unavailable, ${labelDate}` : labelDate;
  const inputEl = useRef(null);

  useEffect(() => {
    if (Number(dayNum) === Number(focusedDayNum)) {
      inputEl.current.focus();
    }
  }, [focusedDayNum]);

  return (
    <button
      ref={inputEl}
      type="button"
      aria-label={label}
      aria-pressed={pressed === -1 ? false : true}
      className={["Calendar-item", bthState].join(" ")}
      data-timestamp={day.unix()}
      data-day={`${dayNum}`}
      data-date={formattedDate}
      onFocus={event => {
        const focused = event.currentTarget.dataset["day"];
        const date = event.currentTarget.dataset["date"];
        if (Number(focusedDayNum) !== Number(focused)) {
          dispatch({ type: "FOCUS_DAY", payload: { focused, date } });
        }
      }}
      onClick={() => {
        dispatch({ type: "SELECT_DATE", payload: yearMonthDay(day) });
        dispatch({
          type: "CALENDAR_UPDATES",
          payload: `selected ${label}`
        });
      }}
      {...currentState}
      {...tabIndex}
    >
      {dayNum}
    </button>
  );
};

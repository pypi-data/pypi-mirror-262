"use client";
import React, { useContext } from "react";
import Select from "react-select";
import roleContext from "../contexts/roleContext";
import { useNavigate } from "react-router-dom";

const Header = () => {
  const navigate = useNavigate();
  const selectContext = useContext(roleContext);

  function handleChange(val) {
    const user = JSON.parse(localStorage.getItem("komodoUser"));
    localStorage.setItem("komodoUser", JSON.stringify({ ...user, select: val }));
    selectContext?.setReactSelect(val);
    selectContext?.setChatGuid("");
    selectContext?.setChatHistory(false);
    selectContext?.setList([]);
    navigate("/chat");
  }

  const style = {
    control: (base) => ({
      ...base,
      cursor: "pointer",
      border: "0",
      fontSize: "21px",
      fontFamily: "Cerebri Sans",
      boxShadow: "none",
      " &: hover": {
        border: "0",
      },
    }),
    option: (base, { isSelected }) => ({
      ...base,
      backgroundColor: isSelected ? "#316ff642" : "#ffffff",
      cursor: "pointer",
      color: isSelected ? "#333" : "#000",
      " &:hover": {
        backgroundColor: "#316ff673",
      },
    }),
    placeholder: (defaultStyles) => {
      return {
        ...defaultStyles,
        fontSize: "5px",
      };
    },
  };

  // flex flex-row md:flex-col-reverse justify-between border-b-[0.5px] border-[#CDCDCD] h-[93px] md:h-auto items-center px-5 md:px-0 md:mx-4 sm:mx-2
  return (
    <div className="flex flex-row md:flex-col-reverse md:-mt-[44px] justify-between border-b-[0.5px] border-[#CDCDCD] h-[93px] md:h-auto items-center px-5 md:px-0">
      <div className="w-full">
        {selectContext?.reactSelect?.purpose !== undefined ? (
          <>
            <div className="w-[330px]">
              <Select
                className="font-cerebriregular"
                value={selectContext?.reactSelect}
                onChange={handleChange}
                options={selectContext?.agentList?.agents}
                styles={style}
                getOptionLabel={(agent) => agent["name"]}
                getOptionValue={(agent) => agent["email"]}
              />
            </div>
            <p className="m-[2px] font-cerebriregular">{selectContext?.reactSelect?.purpose || ""}</p>
          </>
        ) : null}
      </div>
      <div className="pr-1 sm:w-[90%] md:w-[95%] md:ml-10 w-full">
        <div className="flex items-center justify-end space-x-2 w-full">
          <h1 className="text-3xl font-cerebrisemibold">Komodo AI</h1>
        </div>
        <div className="text-[18px] mt-1 font-cerebriregular text-end">
          <p>
            {selectContext?.agentList?.name ? (
              <span>{selectContext?.agentList?.name}</span>
            ) : (
              <span className="opacity-0">Komodo</span>
            )}
          </p>
        </div>
      </div>
    </div>
  );
};

export default Header;

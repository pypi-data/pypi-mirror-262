import React, { useEffect, useRef, useState } from "react";
import profile from "../images/profile.png";
import setting from "../images/setting.png";
import robot from "../images/robot.png";
import chat from "../images/chat.png";
import doc from "../images/doc.png";
import { Link, useNavigate } from "react-router-dom";
import { BiSolidMessageAltDetail } from "react-icons/bi";
import { HiDocumentText } from "react-icons/hi";
import { BsRobot } from "react-icons/bs";
import { FiSettings } from "react-icons/fi";
import { useLocation } from "react-router-dom";

const Sidebar = () => {
  const { pathname } = useLocation();
  const modalRef = useRef(null);
  const [isDropdownOpen, setDropdownOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const handleImageClick = () => {
    navigate("/profile");
    setDropdownOpen(!isDropdownOpen);
  };

  // const handleLogOut = () => {
  //     localStorage.removeItem("komodoUser");
  //     navigate('/');
  //     window.location.reload();
  //     setDropdownOpen(false);
  // }
  const handleClickOutside = (e) => {
    if (modalRef.current && !modalRef.current.contains(e.target)) {
      setDropdownOpen(false);
    }
  };

  return (
    <div className=" bg-[#2E2E2E] px-5 pt-5 w-[68px] xl:w-[60px] h-screen flex flex-col justify-between items-center">
      <div className="gap-10 flex flex-col">
        {pathname !== "/" ? (
          <>
            <Link to="/chat">
              {/* <BiSolidMessageAltDetail
                className={`text-[29px] ${
                  pathname === "/chat" || pathname.includes("/details")
                    ? "text-white"
                    : "text-[#797c8c]"
                }`}
              /> */}
              <img
                src={chat}
                alt="chat"
                className={` ${
                  pathname === "/chat" || pathname.includes("/details")
                    ? "text-white"
                    : "text-[#797c8c]"
                }`}
              />
            </Link>
            <Link to="/chatbot">
              {/* <BsRobot
                className={`text-[29px] ${
                  pathname === "/chatbot" ? "text-white" : "text-[#797c8c]"
                }`}
              /> */}
              <img
                src={robot}
                alt="robot"
                className={`w-[25px] ${
                  pathname === "/chatbot" ? "text-white" : "text-[#797c8c]"
                }`}
              />
            </Link>
            <Link to="/document">
              {/* <HiDocumentText
                className={`text-[30px] ${
                  pathname === "/document" ? "text-white" : "text-[#797c8c]"
                }`}
              /> */}
              <img
                src={doc}
                alt="doc"
                className={` ${
                  pathname === "/document" ? "text-white" : "text-[#797c8c]"
                }`}
              />
            </Link>
          </>
        ) : (
          <BiSolidMessageAltDetail className="text-[29px] text-[#797c8c]" />
        )}
        {/*              
                {pathname !== "/" ? (
                    <Link to='/chatbot'>
                        <BsRobot
                            className={`text-[29px] ${(pathname === "/chat" || pathname.includes("/details"))
                                ? "text-white"
                                : "text-[#797c8c]"
                                }`}
                        />
                    </Link>
                ) : (
                    <BsRobot className="text-[29px] text-[#797c8c]" />
                )} */}
      </div>
      <div className="gap-10 flex flex-col items-center mb-5">
        {/* <FiSettings
          className="text-[29px] text-[#797c8c] cursor-pointer"
          onClick={() => navigate("/settings")}
        /> */}
        <img
          src={setting}
          alt="setting"
          className=" text-[#797c8c] cursor-pointer"
          onClick={() => navigate("/settings")}
        />

        {pathname !== "/" && (
          <div className="">
            <img
              src={profile}
              alt="profile"
              onClick={handleImageClick}
              className="cursor-pointer"
            />

            {/* {isDropdownOpen && (
                            <div ref={modalRef} className="absolute left-20 bottom-5  bg-white border rounded-md shadow-md text-center">
                                <button className='text-[#5A636C] text-[14px] font-cerebri leading-[30px] px-4 py-[2px] mt-1 cursor-pointer' onClick={handleLogOut}>
                                    Log out
                                </button>
                            </div>
                        )} */}
          </div>
        )}
      </div>
    </div>
  );
};

export default Sidebar;

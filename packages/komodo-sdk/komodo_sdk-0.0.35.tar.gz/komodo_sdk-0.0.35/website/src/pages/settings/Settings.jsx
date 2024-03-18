import React, { useRef, useState } from "react";
import Sidebar from "../../components/Sidebar";
import apperance from "../../assets/magicpen.svg";
import setting from "../../assets/setting.svg";
import apperance1 from "../../assets/magicpen-1.svg";
import setting1 from "../../assets/setting-1.svg";
import botAvatar from "../../assets/botAvatar.svg";
import person from '../../../src/images/person.png'
import square from "../../assets/square.svg";
import message from "../../assets/message.svg";
import headphone from "../../assets/headphone.svg";
import grey from "../../assets/grey.svg";
import yellow from "../../assets/yellow.svg";
import parrot from "../../assets/parrot.svg";
import green from "../../assets/green.svg";
import sky from "../../assets/sky.svg";
import blue from "../../assets/blue.svg";
import orange from "../../assets/orange.png";
import pink from "../../assets/pink.svg";
import multi from "../../assets/multi.png";

import CustomInput from "../../components/inputs/CustomInputs";
import { Link } from "react-router-dom";

const Settings = () => {
  const [selectedTab, setSelectedTab] = useState(0);
  const [logoImage, setLogoImage] = useState(null);
  const fileInputRef = useRef(null);

  const handleTabClick = (index) => {
    setSelectedTab(index);
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onloadend = () => {
      setLogoImage(reader.result);
    };
    if (file) {
      reader.readAsDataURL(file);
    }
  };

  const handleChooseFile = () => {
    fileInputRef.current.click();
  };

  console.log("selectedTab", selectedTab);

  const handleChange = () => { };

  return (
    <>
      <div className="flex font-cerebriregular">
        <div>
          <Sidebar />
        </div>

        <div className="flex-1 flex-col h-[100vh] overflow-auto  ">
          <div className="h-100 border-b border-customGray  w-[100%] px-8 xs:px-2 py-4 flex flex-col justify-between gap-3">
            <h2 className="text-[26px] font-cerebri text-blackText leading-[27px]">Settings</h2>

            <h6 className="text-[18px] font-cerebri text-blackText">Settings</h6>
          </div>
          <div className="px-6 xs:px-2 py-10 flex-1">
            <div className="grid grid-cols-1 gap-9">
              <div className="flex bg-lightSky rounded-[10px] p-2 xs:p-1 w-[335px] xs:w-[290px] sm:w-[310px] h-[58px]">
                <div
                  className={`px-5 xs:px-2 xs:py-0 py-2 sm:px-3 sm:text-[16px] flex gap-2 justify-center items-center cursor-pointer rounded-[10px] ${selectedTab === 0 ? "bg-white text-customBlue" : "bg-lightSky"
                    }`}
                  onClick={() => handleTabClick(0)}
                >
                  <img src={selectedTab === 0 ? apperance : apperance1} className="w-5 h-5" alt="" />
                  <span>Appearance</span>
                </div>
                <div
                  className={`px-4 xs:px-2 xs:py-0 py-2 sm:px-3 sm:text-[16px] flex gap-2 justify-center items-center cursor-pointer rounded-[10px] ${selectedTab === 1 ? "bg-white text-customBlue" : "bg-lightSky"
                    }`}
                  onClick={() => handleTabClick(1)}
                >
                  <img src={selectedTab === 0 ? setting : setting1} className="w-5 h-5" alt="" />
                  <span>Other Setting</span>
                </div>
              </div>

              {selectedTab === 0 && (
                <div className="grid grid-cols-1 gap-9">
                  <div className="w-1/4 md:w-[100%]">
                    <CustomInput label="Bot Name *" placeholder="Bot Name" onChange={handleChange} value="" />
                  </div>
                  <div>
                    <p className="text-[18px] mb-3">Bot Avatar </p>
                    <div className="flex gap-4">
                      <img src={logoImage || person} alt="" className="w-[62px] h-[62px] rounded-xl" />
                      <div className="text-[16px] flex flex-col justify-around">
                        <p className="text-customBlue underline cursor-pointer" onClick={handleChooseFile}>
                          Change Logo
                        </p>
                        <p className="text-greyText">JPG/PNG up to 5 MB</p>
                      </div>
                    </div>
                    <input
                      type="file"
                      accept="image/*"
                      ref={fileInputRef}
                      style={{ display: "none" }}
                      onChange={handleFileChange}
                    />
                  </div>
                  {/* <div>
                  <p className="text-[18px] mb-3">Select button icon </p>
                  <div className="flex gap-4">
                    <img src={botAvatar} />
                    <div className="rounded-[10px] border border-customGray w-[72px] flex items-center justify-center">
                      <img src={message} />
                    </div>
                    <div className="rounded-[10px] border border-customGray w-[72px] flex items-center justify-center">
                      <img src={headphone} />
                    </div>
                    <div className="rounded-[10px] border border-customGray w-[72px] flex items-center justify-center">
                      <img src={square} />
                    </div>
                  </div>
                </div> */}

                  <div>
                    <p className="text-[18px] mb-3">Accent Colour </p>
                    <div className="flex gap-4 sm:grid sm:grid-cols-4">
                      <div className="rounded-[10px] border border-customGray xs:w-[62px] xs:h-[62px] w-[72px] h-[72px] flex items-center justify-center ">
                        <img src={grey} alt="" />
                      </div>

                      <div className="rounded-[10px] border border-customGray xs:w-[62px] xs:h-[62px] w-[72px] h-[72px] flex items-center justify-center">
                        <img src={yellow} alt="" />
                      </div>

                      <div className="rounded-[10px] border border-customGray xs:w-[62px] xs:h-[62px] w-[72px] h-[72px] flex items-center justify-center">
                        <img src={parrot} alt="" />
                      </div>

                      <div className="rounded-[10px] border border-customGray xs:w-[62px] xs:h-[62px] w-[72px] h-[72px] flex items-center justify-center">
                        <img src={green} alt="" />
                      </div>

                      <div className="rounded-[10px] border border-customGray xs:w-[62px] xs:h-[62px] w-[72px] h-[72px] flex items-center justify-center">
                        <img src={sky} alt="" />
                      </div>

                      <div className="rounded-[10px] border border-customGray xs:w-[62px] xs:h-[62px] w-[72px] h-[72px] flex items-center justify-center">
                        <img src={blue} alt="" />
                      </div>

                      <div className="rounded-[10px] border border-customGray xs:w-[62px] xs:h-[62px] w-[72px] h-[72px] flex items-center justify-center">
                        <img src={orange} alt="" />
                      </div>

                      <div className="rounded-[10px] border border-customGray xs:w-[62px] xs:h-[62px] w-[72px] h-[72px] flex items-center justify-center">
                        <img src={pink} alt="" />
                      </div>

                      <div className="rounded-[10px] border border-customGray xs:w-[62px] xs:h-[62px] w-[72px] h-[72px] flex items-center justify-center">
                        <img src={multi} alt="" />
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {selectedTab === 1 && (
                <div className="grid grid-cols-1 gap-10 w-1/3 lg:w-[100%] font-cerebriregular text-[16px]">
                  <div>
                    <label htmlFor="language" className="block mb-2">
                      Language
                    </label>
                    <select
                      id="language"
                      className="w-[310px] xs:w-[100%] h-12 p-2 border border-gray-300 rounded-[10px] shadow-sm bg-gray-100 focus:outline-none"
                    // value={selectedLanguage}
                    // onChange={handleLanguageChange}
                    >
                      <option value="English">English</option>
                      <option value="Spanish">Spanish</option>
                      <option value="French">French</option>
                      {/* Add more language options as needed */}
                    </select>
                  </div>

                  <div className="flex justify-between">
                    <p>Always show code when using data analyst</p>
                    <label className="inline-flex items-center cursor-pointer">
                      <input type="checkbox" value="" className="sr-only peer" />
                      <div className="relative w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                    </label>
                  </div>

                  <div className="grid grid-cols-1 gap-6">
                    <div className="flex justify-between items-center">
                      <p>Archived chats</p>
                      <button className="bg-customGray py-2 px-4 rounded-[10px]">Manage</button>
                    </div>

                    <div className="flex justify-between items-center">
                      <p>Archive all chats</p>
                      <button className="bg-customGray py-2 px-4 rounded-[10px]">Archive Al</button>
                    </div>

                    <div className="flex justify-between items-center">
                      <p>Delete all chats</p>
                      <button className="bg-[#E84141] text-white py-2 px-4 rounded-[10px] min-w-[105px] ">
                        Delete All
                      </button>
                    </div>
                  </div>

                  <div className="flex justify-between items-center">
                    <p>Chat history & training</p>
                    <label className="inline-flex items-center cursor-pointer">
                      <input type="checkbox" value="" className="sr-only peer" />
                      <div className="relative w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                    </label>
                  </div>

                  <div className="flex justify-between items-center">
                    <p>Delete Account</p>
                    <button className="bg-[#E84141] text-white py-2 px-4 rounded-[10px]">Delete</button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      <Link to="/privacy" className="text-[#959CB6] text-[16px] absolute bottom-4 right-8">
        Privacy Policy
      </Link>
    </>
  );
};

export default Settings;

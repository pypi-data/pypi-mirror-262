import React, { useContext, useEffect, useRef, useState } from "react";
import AI from "../../assets/ai.png";
import { FiDownloadCloud } from "react-icons/fi";
import profile from "../../images/profile.png";
import send from "../../images/send.png";
import wave from "../../images/wave.png";
import { API_Path } from "../../API/ApiComment";
import roleContext from "../../contexts/roleContext";
import { ErrorToast } from "../../helpers/Toast";
import { ApiGet } from "../../API/API_data";

export const Chat = ({ selectedItemName, selectedFileName }) => {
  const user = JSON.parse(localStorage.getItem("komodoUser"));
  const chatContext = useContext(roleContext);
  const chatContainerRef = useRef(null);

  const [prompt, setPrompt] = useState("");
  const [text, setText] = useState("");
  const [fullMessage, setFullMessage] = useState("");
  const [allChatData, setAllChatData] = useState([]);
  const [newDetails, setNewDetails] = useState({ gId: "", chatRes: "" });

  console.log("fullMessage", fullMessage);
  console.log("allChatData", allChatData);
  // const getConversationByGuid = async (guid) => {
  //     try {
  //         // setLoader(true)
  //         const res = await ApiGet(API_Path.getDeleteConversation + guid)
  //         if (res?.status === 200) {
  //             setAllChatData(res?.data[0]?.messages)
  //         }
  //     } catch (error) {
  //         console.log('user details get ::error', error)
  //         ErrorToast(error?.data?.detail || "Something went wrong")
  //     } finally {
  //         // setLoader(false)
  //     }
  // }
  // useEffect(() => {
  //     getConversationByGuid("bb6b917b-6608-42ea-8e25-c69c2004d374")
  // }, []);
  useEffect(() => {
    if (fullMessage !== "") {
      setNewDetails((perState) => {
        return { ...perState, chatRes: fullMessage };
      });
    }
  }, [fullMessage]);
  const sendPrompt = async () => {
    if (prompt.trim() !== "") {
      if (newDetails.chatRes !== "") {
        setAllChatData((prevData) => [
          ...prevData,
          {
            sender: chatContext?.reactSelect?.shortcode,
            text: newDetails.chatRes,
          },
          { sender: user.email, text: prompt },
        ]);
        setNewDetails({ ...newDetails, chatRes: "" });
      } else {
        setAllChatData((prevData) => [
          ...prevData,
          { sender: user.email, text: prompt },
        ]);
      }
      if (prompt !== "") {
        setText(prompt);
        setPrompt("");
        setFullMessage("");
        let eventSource;

        eventSource = new EventSource(
          `${API_Path.streamedApi}email=${user?.email}&agent_shortcode=${chatContext?.reactSelect?.shortcode}&prompt=${prompt}`
        );

        eventSource.onmessage = (event) => {
          const binaryStr = atob(event.data);
          const bytes = new Uint8Array(
            binaryStr.split("").map((char) => char.charCodeAt(0))
          );
          const newMessage = new TextDecoder("utf-8").decode(bytes);
          setFullMessage((prvMsg) => prvMsg + " " + newMessage);
        };

        eventSource.addEventListener("stream-complete", function (e) {
          eventSource.close();
        });

        eventSource.onopen = (event) => {
          console.log("Connection to server opened.");
        };

        eventSource.onclose = function () {
          console.log("Connection closed by the server.");
        };

        eventSource.onerror = (event) => {
          if (eventSource.readyState === EventSource.CLOSED) {
            console.error("Connection was closed.");
          } else {
            console.error("An error occurred:", event);
          }
          eventSource.close();
        };
        return () => {
          eventSource.close();
        };
      }
    }

    setPrompt("");
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      sendPrompt();
    }
  };

  return (
    <>
      <div className="flex items-center justify-between px-4 py-[11.5px] border-b border-[#E8E9EA]">
        <div className="text-[#1C232D] text-[16px] font-cerebriMedium">
          <div className="text-[#1C232D] text-[16px] font-cerebriMedium">
            {selectedItemName
              ? selectedFileName
                ? `${selectedItemName} / ${selectedFileName}`
                : selectedItemName
              : ""}
          </div>
        </div>

        <div className="flex items-center gap-2 border border-[#4460E3] py-2 px-5 rounded-lg">
          <FiDownloadCloud className="text-[#4460E3] text-[18px]" />
          <div className="text-[#4460E3] font-normal text-[14px] font-cerebri">
            Export saved
          </div>
        </div>
      </div>
      <div className="h-[calc(100vh-239px)] px-5 pt-1">
        <div
          className="chatscreen h-[calc(100vh-165px)] overflow-auto"
          ref={chatContainerRef}
        >
          {allChatData &&
            allChatData.length > 0 &&
            allChatData.map((val, index) => {
              return (
                <div key={index} className="flex flex-col">
                  {val?.sender === user.email && (
                    <div className="flex items-end justify-end">
                      <div className="flex items-start justify-end max-w-[94%] mt-4 gap-1">
                        <div className="flex flex-col">
                          <div className="text-[16px] font-cerebriregular rounded-[10px] bg-[#497ad32b] px-3 py-2 text-customBlue">
                            {val?.text}
                          </div>

                          {/* {val?.time && message?.answer && (
                          <div className="text-blackText font-cerebri font-normal text-[12px] text-right mt-1">
                            {new Date(
                              message.time.seconds * 1000 +
                                message.time.nanoseconds / 1000000
                            ).toLocaleTimeString("en-US", {
                              hour: "2-digit",
                              minute: "2-digit",
                              hour12: true,
                            })}
                          </div>
                        )} */}
                        </div>
                        <img
                          src={profile}
                          className="w-[30px] h-[30px]"
                          alt=""
                        />
                      </div>
                    </div>
                  )}

                  {/* {message.answer && ( */}
                  {val?.sender === chatContext?.reactSelect?.shortcode && (
                    <div className="flex items-start w-full mt-4 gap-2">
                      <img
                        src={wave}
                        className="w-[30px] h-[30px] mb-5"
                        alt=""
                      />
                      <div className="flex flex-col">
                        <div className="text-[16px] font-cerebriregular rounded-[10px] bg-senderBG border border-borderSky   px-3 py-2 text-blackText">
                          {val?.text}

                          {/* {message.answer} */}
                        </div>

                        {/* {message.time && ( */}
                        <div className="text-blackText font-cerebri font-normal text-[12px] text-right mt-1">
                          {/* 10:11 */}
                        </div>
                        {/* )} */}
                      </div>
                    </div>
                  )}

                  {/* //   )} */}
                </div>
              );
            })}
          {text !== "" && fullMessage && (
            <div className="flex items-start w-full mt-4 gap-2">
              <img src={wave} className="w-[30px] h-[30px] mb-5" alt="" />
              <div className="flex flex-col">
                <div
                  className="text-[16px] font-cerebriregular rounded-[10px] bg-senderBG border border-borderSky  px-3 py-2 text-blackText"
                  dangerouslySetInnerHTML={{
                    __html: fullMessage.replace(/\n/g, "<br>"),
                  }}
                >
                  {/* {message.answer} */}
                </div>

                {/* {message.time && ( */}
                <div className="text-blackText font-cerebri font-normal text-[12px] text-right mt-1">
                  {/* 10:11 */}
                </div>
                {/* )} */}
              </div>
            </div>
          )}
          <div className={`flex flex-col mt-4 mb-5 `}>
            {/* {recommendedQuestions.length > 0 &&
        recommendedQuestions.map((question, index) => (
        <div
          key={index}
          className="border border-[#D4E0E9] rounded-lg px-3 py-2 w-fit cursor-pointer mt-2"
          onClick={() => handleRecommendedQuestionClick(question)}
        >
          {question}
        </div>
        ))} */}
          </div>
        </div>
      </div>
      <div className="relative px-5 border-t border-[#F3F4F4] pt-4 flex gap-2">
        <input
          type="text"
          className="border rounded-lg bg-senderBG border-borderSky  py-3.5 px-4 w-full outline-none text-[14px] font-cerebriregular leading-[17.78px]"
          placeholder="Ask or generate anything..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyDown={handleKeyPress}
        />
        <span className="cursor-pointer " onClick={sendPrompt}>
          <img src={send} alt="" />
        </span>
      </div>
    </>
  );
};

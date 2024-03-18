import React, { useState, useEffect, useContext, memo } from 'react';
import roleContext from "../../contexts/roleContext"
import { API_Path } from '../../API/ApiComment';

const EnhancedPrompt = ({ prompt, guid, setNewDetails }) => {
    const user = JSON.parse(localStorage.getItem('komodoUser'))
    const chatContext = useContext(roleContext);
    const [fullMessage, setFullMessage] = useState('');

    useEffect(() => {
        if (prompt !== "") {
            setFullMessage("")
            let eventSource;
            // if (!["", undefined]?.includes(guid)) {
            //     eventSource = new EventSource(`${API_Path.streamedApi}email=${user?.email}&agent_shortcode=${chatContext?.reactSelect?.shortcode}&prompt=${prompt}&guid=${guid}`);
            // } else {
                eventSource = new EventSource(`${API_Path.streamedApi}email=${user?.email}&agent_shortcode=${chatContext?.reactSelect?.shortcode}&prompt=${prompt}`);
            // }

            eventSource.onmessage = (event) => {
                const newMessage = (event.data);
                setFullMessage((prvMsg) => prvMsg + ' ' + newMessage);
            };

            eventSource.addEventListener('stream-complete', function (e) {
                eventSource.close();
                // if (["", undefined]?.includes(guid)) {
                //     chatContext?.conversations(true)
                // }
                // else {
                //     chatContext?.conversations()
                // }
            });

            eventSource.onopen = (event) => {
                console.log('Connection to server opened.');
            };

            eventSource.onclose = function () {
                console.log('Connection closed by the server.');
            };

            eventSource.onerror = (event) => {
                if (eventSource.readyState === EventSource.CLOSED) {
                    console.error('Connection was closed.');
                } else {
                    console.error('An error occurred:', event);
                }
                eventSource.close();
            };
            return () => {
                eventSource.close();
            };
        }
    }, [prompt]);


    // useEffect(() => {
    //     if (fullMessage !== "") {
    //         setNewDetails((perState) => {
    //             return { ...perState, chatRes: fullMessage }
    //         })
    //     }
    // }, [fullMessage])

    return (
        <div className='w-fit text-[#495057]'>
            <p
                className='font-cerebriregular text-[15px] leading-[34px]'
                dangerouslySetInnerHTML={{ __html: fullMessage.replace(/\n/g, '<br>') }}
            ></p>
        </div>
    );
};

export default memo(EnhancedPrompt);
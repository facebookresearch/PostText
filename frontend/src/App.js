import React, { useEffect, useState } from 'react';
import { Terminal } from 'primereact/terminal';
import { TerminalService } from 'primereact/terminalservice';
import { Panel } from 'primereact/panel';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { coy } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { ProgressBar } from 'primereact/progressbar';


import './index.css';

export default function App() {

    const [question, setQuestion] = useState("");
    
    const [sqlBefore, setSQLBefore] = useState("");

    const [sqlAfter, setSQLAfter] = useState("");

    const [sqlResult, setSQLResult] = useState("");

    const [prompt, setPrompt] = useState("");

    const [running, setRunning] = useState(false);


    const commandHandler = (text) => {
        let response;
        let argsIndex = text.indexOf(' ');
        let command = argsIndex !== -1 ? text.substring(0, argsIndex) : text;

        switch (command) {
            // case 'date':
            //     response = 'Today is ' + new Date().toDateString();
            //     break;

            // case 'greet':
            //     response = 'Hola ' + text.substring(argsIndex + 1) + '!';
            //     break;

            // case 'random':
            //     response = Math.floor(Math.random() * 100);
            //     break;

            case 'clear':
                TerminalService.emit('clear');
                break;

            default:
                TerminalService.emit('response', 'Running...');
                setRunning(true);
                fetch("/query?" + new URLSearchParams({query: text})).then((response) => response.json())
                           .then((data) => {
                                setQuestion(text);
                                setPrompt(data.prompt);
                                setSQLBefore(data.sql_before);
                                setSQLAfter(data.sql_after);
                                setSQLResult(data.result);
                                response = 'Prompt: \n\n' + data.prompt + 
                                           '\n\nSQL (Before): \n\n' + data.sql_before + 
                                           '\n\nSQL (After): \n\n' + data.sql_after + 
                                           '\n\nQuery result: \n\n' + data.result;
                                TerminalService.emit('response', 'Done!');
                                setRunning(false);
                            });
                break;
        }

    };

    useEffect(() => {
        TerminalService.on('command', commandHandler);

        return () => {
            TerminalService.off('command', commandHandler);
        };
    }, []);

    return (
        <div className="card posttext-demo">
            <h2>PostText</h2>
            <p>
                Enter a question or "<strong>clear</strong>" to clear all commands.
            </p>
            <Terminal style={{width: '800px', height: '150px'}}welcomeMessage="Welcome to PostText" prompt="posttext $" />

            <ProgressBar mode="indeterminate" style={{ width: '800px', height: '6px', display: running ? '' : 'none' }}></ProgressBar>

            <Panel className="my-3" header="Prompt" toggleable style={{width: '800px', display: prompt === "" ? 'none' : ''}}>
            {/* <p className="my-3">{prompt}</p> */}
            <SyntaxHighlighter language="sql" style={coy}>
              {prompt}
            </SyntaxHighlighter>                 
            </Panel>

            <Panel className="my-3" header="SQL (Before)" toggleable style={{width: '800px', display: sqlBefore === "" ? 'none' : ''}}>
            {/* <p className="my-3">{}</p> */}
            <SyntaxHighlighter language="sql" style={coy}>
              {sqlBefore}
            </SyntaxHighlighter>            
            </Panel>

            <Panel className="my-3" header="SQL (After)" toggleable style={{width: '800px', display: sqlAfter === "" ? 'none' : ''}}>
            {/* <p className="my-3">{sqlAfter}</p> */}
            <SyntaxHighlighter language="sql" style={coy}>
              {sqlAfter}
            </SyntaxHighlighter>            
            </Panel>

            <Panel className="my-3" header="Query result" toggleable style={{width: '800px', display: sqlResult === "" ? 'none' : ''}}>
            {/* <p className="my-3">{sqlResult}</p> */}
            <SyntaxHighlighter language="sql" style={coy}>
              {sqlResult}
            </SyntaxHighlighter>            
            </Panel>


        </div>
    );
}
         

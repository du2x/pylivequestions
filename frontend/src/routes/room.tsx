import React, { useEffect, useState } from "react";

import { wsEndpoint } from '../config'

import Typography from '@material-ui/core/Typography'
import Grid from '@material-ui/core/Grid'
import Box from '@material-ui/core/Box'
import Button from '@material-ui/core/Button'


import { Question, QOption, FQuestion, FQOption } from './../types/Question';
import { getActiveQuestionRoom, postAttempt, getQuestions, postRoomAction } from '../api/rooms-api'
import { useRef } from "react";

interface RoomState {
    name: string,
    question: Question,
    room_id: string,
    token: string,
    answer: string,
    answered: boolean,
    feedback: string,
    questions: FQuestion[],
    owner: string
  }


const qoption: QOption = {ref: '', text: ''}
const qfoption: FQOption = {correct: false, text: '', post_text: ''}
const iq: Question =  {text:'', options: [qoption,], type:'', uuid: ''}
const ifq: FQuestion =  {text:'', options: [qfoption,], type:'', uuid: '', pickedAt: null}

export default function Room(props:any) {
    const [state, setState] = useState<RoomState>({
        question: iq,
        room_id: '',
        token: '',
        name: '',
        answer: '',
        answered: false,
        feedback: '',
        owner: '',
        questions: [ifq]
      });
      
    const webSocket = useRef<WebSocket>();
    
    const fetchQuestions = async() =>{    
      state.questions = await getQuestions(props.location['token']);
      setState({...state})
    }
    
    const fetchActiveQuestion = async() =>{
      try {        
        const question = await getActiveQuestionRoom(props.location['token'], props.match.params['id']);            
        setState({name: props.location['name'], question: question, room_id: props.match.params['id'], token: props.location['token'], answer: '', answered:false, feedback: '', questions: state.questions, owner: props.location['owner']});
      } catch (e) {
        alert(`Failed to fetch question: ${e.message}`)
      }    
  
    }

    useEffect(() => {      
      webSocket.current = new WebSocket(wsEndpoint + '?data='+ props.match.params['id'] + ',' + props.location['username']);
      webSocket.current.onmessage = (message) => {          
        if(message.data == "new question"){
          console.log("fetching new question.")
          fetchActiveQuestion()
        }
        else {
          var aux = state;        
          aux.feedback = message.data;
          setState({...aux});
        }
      };
      
        fetchActiveQuestion();
        fetchQuestions();        
      }, []);      


      const handleSubmit = () => {        

        console.log('handling submit' + JSON.stringify(state))

        async function makeAttempt() {        
          const room_id = props.match.params['id']
          const data = {
            question_uuid: state.question.uuid,
            room_id: room_id,
            answer: state.answer
          }
          await postAttempt(state.token, data);          
      }    
    
        makeAttempt();
        var aux = state;        
        aux.answered = true;
        setState({...aux})
      };

      const handleTextChange = (event: any) => {
          var aux = state;        
          aux.answer = event.target.value;
          setState({...aux});  
      }      
    
      const pickQuestionClicked = (value: string) => {        
        var data = {'action': 'pick', 'question_uuid': value};
        postRoomAction(state.token, state.room_id, data);
      }

      const showFeedbackClicked = () => {        
        var data = {'action': 'close-question'};
        postRoomAction(state.token, state.room_id, data);
      }

      const ownerWidget = () => {
        if(props.location['username'] == props.location['owner']) {
          return (
              <span>room owner: {props.location['owner']} (you)</span>
            )
        }
        else {
          return (
              <span>room owner: {props.location['owner']}</span>
          )
        }
      }
      

      const setQuestionAnswer = (val: string) => {        
        var aux = state;        
        state.answer = val;
        state.answered = false; 
        setState({...aux})
      }
    
      const renderQuestionOptions = () => {
        if(props.location['username'] != props.location['owner']) {
          if(state.question.type==='discursive')
              return <input name="answer" onChange={handleTextChange} />
          if(state.question.type==='single_answer')
              return state.question.options.map(function(option, index){
                  return <div key={index}><label> <input onChange={e => setQuestionAnswer(e.target.value)} type="radio" value={index} name="answer"></input>{option.text}</label></div>
          })
          if(state.question.type==='multiple_answer')
              return state.question.options.map(function(option, index){
                  return <div key={index}><label> <input onChange={e => setQuestionAnswer(e.target.value)} type="checkbox" value={index} name="answer"></input>{option.text}</label></div>
          })  
        }
      };
    
      const renderSubmitButton = () => {        
        if(props.location['username'] != props.location['owner'])        
          if(!state.answered)
            return <input type="submit" value="Send" /> 
          else
            return <p>You have already answered. Wait for feedback. You can also change your answer.</p>
      }

      const renderQuestionPicker = () => {
        {  
            if(props.location['username'] == props.location['owner']){
              return (                                           
              state.questions.map(function(q, index){
                return (
                  <div key={index}>
                    <span>Text: {q.text}</span>
                    <Button value={q.uuid} onClick={e => pickQuestionClicked(e.currentTarget.value)} variant="contained" color="primary">Pick Question</Button>
                  </div>
                
                )
              })
              )            
            }
            else return (<div></div>)
        }
      }


      const renderShowFeedback = () => {
        {  
            if(props.location['username'] == props.location['owner']){
              return (                                           
                  <div>                    
                    <Button onClick={e => showFeedbackClicked()} variant="contained" >Show Feedback</Button>
                  </div>
                
              )            
            }
            else return (<div></div>)
        }

      }
      
           

    return ( 
        <>
       <Grid container direction="column" >
        <Grid container direction="column" justify="center" alignItems="center">
          <Box m={2}>
          <Typography variant="h3">Room "{state.name}"</Typography>
          </Box>
        </Grid>
        <Grid container direction="column" justify="center" >
         <Box m={2}>
           {ownerWidget()}
          </Box>
        </Grid>
        <Grid container direction="column" justify="center" alignItems="center">
         <Box m={2}>
            <Typography variant="h5">Current question: </Typography>
          </Box>
          <Box m={2}>
          <Typography variant="h5">{state.question.text}</Typography>          
          </Box>
        </Grid>
        <Grid container direction="column" justify="center" alignItems="center">
         <Box m={2}>
          <form onSubmit={e => { e.preventDefault(); handleSubmit();}}>        
          {renderQuestionOptions()}
          {renderSubmitButton()}
          </form>
          {renderShowFeedback()}
        </Box>
        </Grid>
        <Grid container direction="column" justify="center" alignItems="center">
         <Box m={2}>

          <div>
              <pre>
               Feedback: {JSON.stringify(state.feedback)}
              </pre>
          </div>
          <div>
            { renderQuestionPicker()}
          </div>
          </Box>
          </Grid>
        </Grid>

        </>
    )

}

import { apiEndpoint } from '../config'
import { Room } from '../types/Room';
import Axios from 'axios'
import { Question, FQuestion } from '../types/Question';


export async function getQuestions(idToken: string): Promise<FQuestion[]> {
  console.log('Fetching questions')

  const response = await Axios.get(`${apiEndpoint}/questions`, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${idToken}`
    },
  })
  
  console.log(response.data.message);
  return response.data.message;
}

export async function getRooms(idToken: string): Promise<Room[]> {
  console.log('Fetching rooms')

  const response = await Axios.get(`${apiEndpoint}/rooms`, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${idToken}`
    },
  })
  
  return response.data.message;
}


export async function getActiveQuestionRoom(idToken: string, idRoom: string): Promise<Question> {
  console.log('Fetching active question')

  const response = await Axios.get(`${apiEndpoint}/room/${idRoom}`, {
    headers: {
      Authorization: `Bearer ${idToken}`,
    },
  });  
    
  return response.data.message;
}


export async function postAttempt(idToken: string, data: any): Promise<string> {
  console.log('Posting attempt ' + idToken)
  console.log(JSON.stringify(data))

  const response = await fetch(`${apiEndpoint}/attempts`, {
    method: 'post',
    headers: {      
      'Content-Type': 'application/json',
      Authorization: `Bearer ${idToken}`,
    }, body: JSON.stringify(data)
  });              

  return response.json();
}


export async function postRoomAction(idToken: string, idRoom: string, data: any): Promise<string> {  
  const response = await fetch(`${apiEndpoint}/room/${idRoom}`, {
    method: 'post',
    headers: {      
      'Content-Type': 'application/json',
      Authorization: `Bearer ${idToken}`,
    }, body: JSON.stringify(data)
  });              

  return response.json();
}



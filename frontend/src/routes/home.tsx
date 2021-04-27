import React, { useContext } from 'react'

import { useHistory } from 'react-router-dom'

import { makeStyles } from '@material-ui/core/styles'

import Typography from '@material-ui/core/Typography'
import Grid from '@material-ui/core/Grid'
import Box from '@material-ui/core/Box'
import Button from '@material-ui/core/Button'
import { Link } from 'react-router-dom';
import { getRooms } from '../api/rooms-api'
import { Room } from '../types/Room'

import { AuthContext } from '../contexts/authContext'
import { useEffect } from 'react'
import { useState } from 'react'

const useStyles = makeStyles((theme) => ({
  root: {},
  title: {
    textAlign: 'center',
  },
  session: {
    width: '80vw',
    overflow: 'auto',
    overflowWrap: 'break-word',
    fontSize: '16px',
  },
  sessionHalf: {
    width: '40vw',
    overflow: 'auto',
    overflowWrap: 'break-word',
    fontSize: '16px',
  },

  hero: {
    width: '100%',
    background: 'rgb(220,220,220)',
  },
}))


interface RoomsState {
  rooms: Room[],
  token: string
}


export default function Home() {

  const auth = useContext(AuthContext)

  const [state, setState] = useState<RoomsState>({rooms: [], token: auth.sessionInfo?.accessToken || ''})
  
  const classes = useStyles()

  const history = useHistory()


  function signOutClicked() {
    auth.signOut()
    history.push('/')
  }

  function changePasswordClicked() {
    history.push('changepassword')
  }



  useEffect(() => {
    async function  fetchRooms() {  
      try {
        const rooms = await getRooms(state.token);
        
        if(rooms) 
          setState({rooms: rooms, token: state.token});    


      } catch (e) {
        alert(`Failed to fetch todos: ${e.message}`)
      }    
    }
  
    fetchRooms();
  }, []);  

  return (
    <Grid container>
      <Grid className={classes.root} container direction="column" justify="center" alignItems="center">
        <Typography variant="h2">Welcome to PyliveQuestions</Typography>        

        <Box m={2}>
          <Button onClick={signOutClicked} variant="contained" color="primary">
            Sign Out
          </Button> 
          <Button onClick={changePasswordClicked} variant="contained" color="primary">
            Change Password
          </Button>
        </Box>                  
        <Box m={1}>
          <Typography variant="h6">Access Token</Typography>
          <pre className={classes.session}>{JSON.stringify(auth.sessionInfo?.accessToken, null, 2)}</pre>
        </Box>
        <Box m={1}>
          <Typography variant="h6">User Info</Typography>
          <pre className={classes.session}>{JSON.stringify(auth.attrInfo)}</pre>
        </Box>
        <Grid container>
          <Grid item xs={6} className={classes.root} container direction="column">
            <Box m={6}>
            <Typography variant="h4">Instructions</Typography>
              <p>Inside the room you create, you can pick the question you want to be answered by the other in the room, </p>
              <p>and you can give the feedback whenever you want.</p>
              <p>There will be always only one CURRENT question in a room. FOCUS guys!</p>
              <Typography variant="h5">Create Room</Typography>
              <p>The UI lacks functionality for creating room. You can create with:</p>
              <pre className={classes.sessionHalf}>curl 'https://b5i7oe5cjg.execute-api.us-east-1.amazonaws.com/dev/rooms' --request POST --data '&#123;"name":"Cool room name"&#125;'' -H "Authorization: Bearer $TOKEN"</pre>
              <Typography variant="h5">Pick Question</Typography>
              <p>When you enter in a room which you are creator, you will be able to Pick Questions.</p>
              <p>When you click the Pick Question button, the choosen question will be automatically be shown to the other users in the room.</p>
              <p>There are some few questions over there you to pick, but you can create others if you want.</p>
              <pre className={classes.sessionHalf}>curl 'https://b5i7oe5cjg.execute-api.us-east-1.amazonaws.com/dev/questions' --request POST --data '&#123;"text":"How many continents are there?", "options": [ &#123;"text": "1", "correct": false, "post_text": "Pangea is past!"&#125;, &#123;"text": "4", "correct": false, "post_text": "You are missing something"&#125;, &#123;"text": "7", "correct": true, "post_text": "Yes! Asia, South America, Europe, North America, Oceania, Central America and Antartic."&#125; ]&#125;' -H "Authorization: Bearer $TOKEN"</pre>
              <Typography variant="h5">Show feedback</Typography>
              <p>When you think there were time enougth to the others answer the current question, you can pick another question, or show feedback to the others by clicking "Show feedback" button. (Feedback is a text that comes along with the options of the question data)</p>
              <Typography variant="h5">Close Room</Typography>
              <p>When you end your use of the room, it is appropriate that you close it.</p>
              <p>The UI lacks functionality for closing room. You can create with:</p>
              <pre className={classes.sessionHalf}>curl 'https://b5i7oe5cjg.execute-api.us-east-1.amazonaws.com/dev/room/your-room-id' --request POST --data '&#123;"action":"close-room"&#125;'' -H "Authorization: Bearer $TOKEN"</pre>
              <Typography variant="h4">Suggested tour</Typography>
              <p>1. create a room with one browser (say chrome)</p>
              <p>2. open the app with another browser (say firefox) and signup with another user</p>
              <p>3. In chrome, enter the room you created.</p>
              <p>4. In firefox, enter the room you created with the first user.</p>
              <p>5. In chrome, pick a question.</p>
              <p>6. In firefox, see the question appears. Answer it.</p>
              <p>7. In chrome, see the message about the another user answer. Click on show feedback.</p>
              <p>8. In firefox, see the feedback.</p>
            </Box>
          </Grid>
          <Grid item xs={6}>

        <Box m={6}>
          <Typography variant="h4">Rooms</Typography>
          <ul>
          {
          state.rooms.map(function(room, index){          

          const newTo = { 
            pathname: '/room/' + room.uuid, 
            name: room.name,
            token: state.token,
            username: auth.attrInfo[0]['Value'],
            owner: room.owner
          };          
          if(room.state!="room_closed")
            return <li key={index}>
                  <Link to={newTo}>{room.name}</Link>
                </li>              
          else
            return <li key={index}>             
            {room.name} (closed)
          </li>              

        })
      }      
        </ul>
        </Box>
        </Grid>
      </Grid>
    </Grid>
    </Grid>
  )
}

import axios from 'axios'
import { useSnackbar } from 'notistack'
import { useEffect, useState } from 'react'
import { Flex } from '@tremor/react'

import './App.css'
import PricePlot from './components/PricePlot'
import Profile from './components/Profile'
import SearchBar from './components/SearchBar'
import UserOperations from './components/UserOperations'

function App() {
  const { enqueueSnackbar, closeSnackbar } = useSnackbar();

  const [user, setUser] = useState({id: -1});
  const [company, setCompany] = useState({figi: 'BBG006L8G4H1', name: 'Яндекс', ticker: 'YNDX'});
  const [operations, setOperations] = useState([]);
  const [update_operations, setUpdateOperations] = useState(true);
  const [update_profile, setUpdateProfile] = useState(true);

  const login = (user) => {
    setUser(user);
    setOperations([]);
    turnOnFlags();
  };

  const turnOnFlags = () => {
    setUpdateOperations(true);
    setUpdateProfile(true);
  };

  useEffect(() => {
    const getData = async () => {
      const response_ = await axios.get('http://localhost:2000/users/' + user.id).catch((error) => {
          // enqueueSnackbar('App\n' + error, {variant: 'error'});
      });
      const user_ = response_.data;
      setUser(user_);
    };
    getData();
  }, [update_profile]);

  return (
    <>
      <h1>ProfiTrade</h1>
      <Flex
        flexDirection='row'
        alignItems='stretch'
      >
        <Profile
          user={user}
          operations={operations}
          updatedProfile={() => setUpdateProfile(false)}
          updateFlag={update_profile}
          setUser={(user) => login(user)}
        />
        <Flex flexDirection='col'>
          <SearchBar
            setCompany={setCompany}
          />
          <Flex
            flexDirection='row'
            alignItems='stretch'
          >
            <PricePlot
              user={user}
              company={company}
              needUpdate={() => turnOnFlags()}
            />
            <UserOperations
              user={user}
              company={company}
              operations={operations}
              setOperations={setOperations}
              updatedOperations={() => setUpdateOperations(false)}
              updateFlag={update_operations}
            />
          </Flex>
        </Flex>
      </Flex>
    </>
  );
}

export default App;

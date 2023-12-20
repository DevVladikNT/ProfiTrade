import { useEffect, useState } from 'react'
import { Flex, Title } from '@tremor/react'

import './App.css'
import SearchBar from './components/SearchBar'
import PricePlot from './components/PricePlot'
import UserOperations from './components/UserOperations'

function App() {
  const user_id = 1;
  const [company, setCompany] = useState({figi: 'BBG006L8G4H1', name: 'Яндекс', ticker: 'YNDX'});
  const [update_operations, setUpdateOperations] = useState(false);

  return (
    <>
      <h1>ProfiTrade</h1>
      <Flex flexDirection='col'>
        <SearchBar
          setResult={setCompany}
        />
        <Flex flexDirection='row'>
          <PricePlot
            userId={user_id}
            company={company}
            needUpdateOperations={() => setUpdateOperations(true)}
          />
          <UserOperations
            userId={user_id}
            updatedOperations={() => setUpdateOperations(false)}
            updateFlag={update_operations}
          />
        </Flex>
      </Flex>
      
    </>
  );
}

export default App;

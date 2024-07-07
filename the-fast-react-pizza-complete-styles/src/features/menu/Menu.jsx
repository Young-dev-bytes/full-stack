import { useLoaderData } from 'react-router-dom';
import { getMenu } from '../../services/apiRestaurant';

import MenuItem from './MenuItem';

function Menu() {
  const menu = useLoaderData();
  console.log('useLoaderData');

  return (
    <ul className="divide-y divide-stone-200 px-2">
      {menu.map((pizza) => {
        return <MenuItem pizza={pizza} key={pizza.id} />;
      })}
    </ul>
  );
}

export async function loader() {
  const menuData = await getMenu();
  console.log(menuData);
  console.log('get menuloader');
  return menuData;
}

export default Menu;

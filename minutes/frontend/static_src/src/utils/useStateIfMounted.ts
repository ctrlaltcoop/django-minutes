import {Dispatch, SetStateAction, useState} from 'react';
import {useEffect, useRef} from 'react';

function useIsComponentMounted() {
  const isMounted = useRef<boolean>(false);
  useEffect(() => {
    isMounted.current = true;
    return () => { isMounted.current = false };
  }, []);
  return isMounted;
}

/**
 * Like React's [useState](https://reactjs.org/docs/hooks-reference.html#usestate)
 * but it makes sure the component that uses this hook is mounted when updating state
 *
 * @see https://reactjs.org/docs/hooks-reference.html#usestate
 * @export
 * @param {any} initialValue
 * @returns {[any, Dispatch<any>]} an array of 2 items
 * the first is the current state, the second is a function that enables
 * updating the state if the component is not mounted
 */
export default function useStateIfMounted<T>(initialValue: T): [T, Dispatch<SetStateAction<T>>] {
  const isComponentMounted = useIsComponentMounted();
  const [state, setState] = useState<T>(initialValue);

  function newSetState(value: SetStateAction<T>) {
    if (isComponentMounted.current) {
      setState(value);
    }
    return value
  }

  return [state, newSetState]
}